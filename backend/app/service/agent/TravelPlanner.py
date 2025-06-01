__all__ = ["TravelPlannerAgent", "graph_executor"]

import json
from typing import Dict, Optional, TypedDict
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from langchain.memory import ConversationBufferMemory
from core.config import env

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from core.config import SESSION_MEMORIES
from langgraph.graph import StateGraph
from langchain.agents import AgentExecutor
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent


class TravelState(TypedDict):
    location: Optional[str]
    period: Optional[str]
    companion: Optional[str]
    style: Optional[str]
    completed: bool


class TravelPlannerAgent:
    """
    AgentService는 하나의 대화 세션을 관리하는 실질적인 Agent 부분입니다.
    그렇기에 채팅 단위로 AgentService를 생성하고 관리합니다.
    """

    def __init__(
        self,
        session_id: str = "test",
        location: Optional[str] = None,
        period: Optional[str] = None,
        companion: Optional[str] = None,
        style: Optional[str] = None,
    ):
        self.session_id = session_id
        self.graphState = TravelState(
            location=location,
            period=period,
            companion=companion,
            style=style,
            completed=False,
        )

    def get_weather(city: str) -> str:
        """Get weather for a given city."""
        return f"It's always sunny in {city}!"

    async def get_main_agent(self):
        agent = create_react_agent(
            f"{env.LLM_PROVIDER}:{env.LLM_MODEL}",
            tools=[self.get_weather],
            checkpointer=InMemorySaver(),
        )
        return agent

    def build_graph(self):
        graph = StateGraph()
        graph.add_node("planner", self.travel_planner_node)
        graph.add_node("attraction", self.tourist_attraction_node)
        graph.add_node("calendar", self.calendar_node)
        graph.set_entry_point("planner")
        graph.add_edge(
            "planner", "attraction", condition=lambda state: state["completed"]
        )
        graph.add_edge(
            "attraction", "calendar", condition=lambda state: state["completed"]
        )
        graph.add_edge(
            "calendar", "planner", condition=lambda state: not state["completed"]
        )
        return graph.compile()

    async def initialize_session_memory(self):
        SESSION_MEMORIES[self.session_id] = ConversationBufferMemory(
            memory_key="history", return_messages=True
        )

    async def initialize_session_memory(self):
        SESSION_MEMORIES[self.session_id] = ConversationBufferMemory(
            memory_key="history", return_messages=True
        )

    async def travel_planner_node(self, state: TravelState, message: str):
        """여행 일정 수립 노드 (비동기, LLM 발화 포함)"""
        memory = SESSION_MEMORIES.get(self.session_id)
        llm = ChatOpenAI(temperature=0, model="gpt-4", streaming=True)
        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""
            당신은 여행 일정을 수립하는 AI 플래너입니다.

            {history}
            사용자: {input}
            AI:""",
        )
        chain = ConversationChain(llm=llm, memory=memory, prompt=prompt, verbose=True)

        async def event_generator():
            async for chunk in chain.astream({"input": message}):
                if chunk.get("response"):
                    yield ServerSentEvent(
                        data=json.dumps(
                            {"message": chunk["response"], "terminated": False}
                        ),
                        event="message",
                    )
            yield ServerSentEvent(
                data=json.dumps({"message": "", "terminated": True}), event="end"
            )

        return EventSourceResponse(event_generator())

    async def tourist_attraction_node(self, state: TravelState):
        """관광명소 검색 노드 (비동기 예시)"""
        attractions = f"[{state.location}] 주변 관광명소 5곳 추천"
        yield ServerSentEvent(
            data=json.dumps({"message": attractions, "terminated": True}),
            event="message",
        )

    async def calendar_node(self, state: TravelState):
        """캘린더 등록 노드 (비동기 예시)"""
        calendar_result = f"일정을 {state.period}에 캘린더에 등록 완료!"
        yield ServerSentEvent(
            data=json.dumps({"message": calendar_result, "terminated": True}),
            event="message",
        )

    async def run(self):
        graph = StateGraph(self.graphState)

        graph.add_node("planner", self.travel_planner_node)
        graph.add_node("attraction", self.tourist_attraction_node)
        graph.add_node("calendar", self.calendar_node)

        graph.set_entry_point("planner")
        graph.add_edge("planner", "attraction", condition=lambda state: state.completed)
        graph.add_edge(
            "attraction", "calendar", condition=lambda state: state.completed
        )
        graph.add_edge(
            "calendar", "planner", condition=lambda state: not state.completed
        )

        executor = graph.compile()
        state = self.graphState

        # 사용자 입력 시뮬레이션
        messages = ["서울", "7월 20일", "가족", "휴양"]
        for msg in messages:
            output = await executor.astep(state, msg)  # 비동기 스텝
            print(output)

    async def event_generator_error(self, error_message: str):
        yield ServerSentEvent(
            data=json.dumps({"error": error_message, "terminated": True}), event="error"
        )

    async def get_agent_response(self, user_query: str):
        memory = SESSION_MEMORIES.get(self.session_id)
        if not memory:
            return EventSourceResponse(self.event_generator_error("Invalid session ID"))

        # 📜 프롬프트
        template = """당신은 친절한 AI 챗봇입니다.

    {history}
    Human: {input}
    AI:"""

        prompt = PromptTemplate(input_variables=["history", "input"], template=template)

        # 🔗 체인 생성
        llm = ChatOpenAI(
            temperature=0, model="gpt-4", api_key=env.OPENAI_API_KEY, streaming=True
        )

        chain = ConversationChain(llm=llm, memory=memory, prompt=prompt, verbose=True)

        async def event_generator():
            try:
                async for chunk in chain.astream({"input": user_query}):
                    if chunk.get("response"):
                        yield ServerSentEvent(
                            data=json.dumps(
                                {"message": chunk["response"], "terminated": False}
                            ),
                            event="message",
                        )
                # 스트리밍 완료
                yield ServerSentEvent(
                    data=json.dumps({"message": "", "terminated": True}), event="end"
                )
            except Exception as e:
                yield ServerSentEvent(
                    data=json.dumps({"error": str(e), "terminated": True}),
                    event="error",
                )

        return EventSourceResponse(event_generator())

    async def event_generator_error(error_message: str):
        yield ServerSentEvent(
            data=json.dumps({"error": error_message, "terminated": True}), event="error"
        )
