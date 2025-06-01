import asyncio
import os
from langgraph.graph import Graph
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Optional, Literal, Annotated, Union
from openai import OpenAI
from pydantic import BaseModel, Field
from langchain_core.tools.base import BaseTool
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langgraph.prebuilt import tools_condition, create_react_agent, ToolNode
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.output_parsers import JsonOutputToolsParser
from langchain.chains import ConversationChain
from enum import StrEnum
from core.config import env
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages


from app.service.agent.prompt.tool.decision_tool_usage import (
    PROMPT as DECISION_TOOL_USAGE_PROMPT,
)
from app.service.agent.prompt.common._llm_guardrail import LLM_GUARDRAIL


class LOCATION_CATEGORY(StrEnum):
    관광명소 = "관광명소"
    음식점 = "음식점"
    카페 = "카페"
    문화시설 = "문화시설"
    숙박 = "숙박"


class TravelState(TypedDict):
    messages: Annotated[list, add_messages]
    location: Optional[str]
    period: Optional[str]
    companion: Optional[str]
    style: Optional[str]
    plan_completed: bool = False
    tool_name: Optional[str] = None


# ===============================================
# Node Functions
# ===============================================
def decide_tool_usage(state: TravelState) -> TravelState:
    """Decide which tool to use based on the user's query."""

    class DecisionToolUsage(BaseModel):
        tool_name: str = Field(..., description="The name of the tool to use")
        answer: Optional[str] = Field(
            None, description="When tool_name is not_use_tool, generate answer "
        )

    llm = init_chat_model(
        model=env.LLM_MODEL,
        model_provider=env.LLM_PROVIDER,
        temperature=0.0,
        max_tokens=200,
    ).with_structured_output(DecisionToolUsage)

    # 시스템 프롬프트를 포함한 메시지 리스트 생성
    messages = [
        ("system", DECISION_TOOL_USAGE_PROMPT.format(LLM_GUARDRAIL=LLM_GUARDRAIL))
    ]
    if state.get("messages"):
        messages.extend(state["messages"])

    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | llm
    response = chain.invoke({"messages": messages})
    return {
        "messages": [AIMessage(content=response.answer)],
        "tool_name": response.tool_name,
        "answer": response.answer,
        "plan_completed": False,
    }


def route_add_conditional_edges(state: TravelState) -> TravelState:
    if state["tool_name"] == "plan_travel_itinerary":
        return "plan_travel_itinerary"
    elif state["tool_name"] == "search_location_by_map":
        return "search_location_by_map"
    elif state["tool_name"] == "not_use_tool":
        return "not_use_tool"
    else:
        return "not_use_tool"


# ===============================================
# Tools
# ===============================================
@tool
def plan_travel_itinerary(
    location: str, period: str, companion: str, style: str
) -> str:
    """Plan a travel itinerary for a given location, period, companion, and style."""
    return f"Travel itinerary for {location} on {period} with {companion} in {style} style."


@tool
def user_map_tools(user_query: str, period: str, category: LOCATION_CATEGORY) -> str:
    """Find sightseeing spots for a given location and date."""
    return f"Sightseeing spots for {user_query} on {period}."


@tool
def use_calendar_tools(
    user_query: str, period: str, category: LOCATION_CATEGORY
) -> str:
    """Find sightseeing spots for a given location and date."""
    return f"Sightseeing spots for {user_query} on {period}."


@tool
def share_travel_itinerary(
    location: str, period: str, companion: str, style: str
) -> str:
    """Share a Complted travel itinerary for a given location, period, companion, and style."""
    return f"Travel plan shared for {location} on {period} with {companion} in {style} style."


@tool
def not_use_tool(user_query: str) -> str:
    """Not related with travel itinerary, just answer the question."""
    return f"Not use tool."


mainTools = [
    plan_travel_itinerary,
    user_map_tools,
    use_calendar_tools,
    share_travel_itinerary,
    not_use_tool,
]


@tool
def plan_travel(location: str, period: str, companion: str, style: str) -> str:
    """Plan a travel itinerary for a given location, period, companion, and style."""
    return f"Travel itinerary for {location} on {period} with {companion} in {style} style."


@tool
def search_location_by_map(
    user_query: str, period: str, category: LOCATION_CATEGORY
) -> str:
    """Find sightseeing spots for a given location and date."""
    return f"Sightseeing spots for {user_query} on {period}."


@tool
def recommend_next_location(
    current_location: str, current_time: str, current_category: LOCATION_CATEGORY
) -> str:
    """Recommend next location for a given location, period, companion, and style."""
    return f"Recommend next location for {current_location} on {current_time} with {current_category}."


@tool
def calculate_travel_time(start_location: str, end_location: str) -> str:
    """Calculate travel time between two locations."""
    return f"Travel time between {start_location} and {end_location}."


@tool
def register_schedule_on_calendar(
    location: str, period: str, companion: str, style: str
) -> str:
    """Register a calendar for a given location, period, companion, and style."""
    return f"Calendar registered for {location} on {period} with {companion} in {style} style."


@tool
def modify_schedule_on_calendar(
    location: str, period: str, companion: str, style: str
) -> str:
    """Modify a calendar for a given location, period, companion, and style."""
    return f"Calendar modified for {location} on {period} with {companion} in {style} style."


@tool
def delete_schedule_on_calendar(
    location: str, period: str, companion: str, style: str
) -> str:
    """Delete a calendar for a given location, period, companion, and style."""
    return f"Calendar deleted for {location} on {period} with {companion} in {style} style."


@tool
def share_travel_plan(location: str, period: str, companion: str, style: str) -> str:
    """Share a travel plan for a given location, period, companion, and style."""
    return f"Travel plan shared for {location} on {period} with {companion} in {style} style."


plan_travel_tools = [plan_travel, recommend_next_location]
map_tools = [search_location_by_map]
calendar_tools = [
    register_schedule_on_calendar,
    modify_schedule_on_calendar,
    delete_schedule_on_calendar,
    share_travel_plan,
]


def wait_user_input_decide_tool_usage(state: TravelState) -> TravelState:
    state["requires_user_input"] = True
    state.pop("tool_name", None)
    state.pop("plan_completed", None)
    state.pop("messages", None)

    return state


# def build_graph():

#     graph = StateGraph(TravelState)
#     graph.add_node(
#         "wait_user_input_decide_tool_usage", wait_user_input_decide_tool_usage
#     )
#     # graph.add_edge(START, "wait_user_input_decide_tool_usage")
#     graph.add_node("decide_tool_usage", decide_tool_usage)
#     graph.add_edge(START, "decide_tool_usage")
#     graph.add_edge("wait_user_input_decide_tool_usage", "decide_tool_usage")
#     graph.add_conditional_edges(
#         "decide_tool_usage",
#         path=route_add_conditional_edges,
#         path_map={
#             "plan_travel": "plan_travel",
#             "search_location_by_map": "search_location_by_map",
#             "not_use_tool": "wait_user_input_decide_tool_usage",
#         },
#     )

#     graph.add_node("plan_travel", plan_travel)
#     graph.add_node("search_location_by_map", search_location_by_map)
#     # graph.add_node("recommend_next_location", recommend_next_location)
#     # graph.add_node("calculate_travel_time", calculate_travel_time)
#     # graph.add_node("register_schedule_on_calendar", register_schedule_on_calendar)
#     # graph.add_node("modify_schedule_on_calendar", modify_schedule_on_calendar)
#     # graph.add_node("delete_schedule_on_calendar", delete_schedule_on_calendar)
#     # graph.add_node("share_travel_plan", share_travel_plan)
#     # graph.set_entry_point("decide_tool_usage")
#     # graph.add_edge("decide_tool_usage", "plan_travel", condition=lambda state: state["tool_name"] == "plan_travel")
#     # graph.add_edge("decide_tool_usage", "search_location_by_map", condition=lambda state: state["tool_name"] == "search_location_by_map")
#     return graph.compile()


# executor = build_graph()


class ChatState(TypedDict):
    """대화 상태를 나타내는 클래스"""

    messages: list[
        Union[HumanMessage, AIMessage, SystemMessage]
    ]  # 대화 메시지 히스토리
    memory: MemorySaver  # 메모리 저장소
    current_tool: Optional[str] = None  # 현재 사용 중인 도구
    tool_result: Optional[str] = None  # 도구 실행 결과
    plan_completed: bool = False  # 계획 완료 여부


# LangGraph: Node 함수
async def chat_node(state: ChatState):
    user_input = state["messages"][-1].content  # 마지막 메시지가 user_input

    llm = ChatOpenAI(
        streaming=True,
        temperature=0.7,
    )

    response = ""
    async for chunk in llm.astream(user_input):
        delta = chunk.choices[0].delta.content or ""
        response += delta
        yield {"response": delta}

    # 메모리에 AI 메시지 저장
    state["messages"].append(AIMessage(content=response))
    state["memory"].messages.append(AIMessage(content=response))

    yield state


# LangGraph: Graph 빌더
def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("chat", chat_node)
    graph.set_entry_point("chat")
    return graph.compile()


# for event in executor.stream({"user_query": "안녕!"}):
#     for key, value in event.items():
#         if "answer" in value and value["answer"] is not None:
#             print(value["answer"])
#         else:
#             print(value)

# executor.get_graph().draw_mermaid_png(output_file_path="graph.png")
