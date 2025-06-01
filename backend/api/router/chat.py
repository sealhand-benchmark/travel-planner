import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Query, Request
import uuid
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from api.schema.chat import ResponsePostChatInitConfig
from langgraph.checkpoint.memory import InMemorySaver
from app.service.agent.test import build_graph
from langgraph.prebuilt import create_react_agent
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from langchain_core.messages import SystemMessage, HumanMessage
from app.service.agent.prompt.tool.decision_tool_usage import (
    PROMPT as DECISION_TOOL_USAGE_PROMPT,
)
from app.service.agent.prompt.common._llm_guardrail import LLM_GUARDRAIL


chat_router = APIRouter()


@chat_router.post(
    path="/session_id",
    summary="세션 아이디 생성",
    description="세션 아이디 생성",
    response_model=ResponsePostChatInitConfig,
)
async def post_chat_session_id(
    request: Request,
):
    session_id = str(uuid.uuid4())
    return ResponsePostChatInitConfig(
        session_id=session_id,
        session_created_at=datetime.now(timezone.utc),
    )


graph = build_graph()


@chat_router.get(
    path="/response",
    summary="대화 응답 요청",
    description="대화 응답 요청",
)
async def chat(
    request: Request,
    session_id: str = Query(...),
    user_input: str = Query(...),
):
    from app.server import memory_store
    from app.service.agent.TravelPlanner import TravelPlannerAgent

    if session_id not in memory_store:
        memory_store[session_id] = InMemorySaver()
        memory_store[session_id].messages = [
            SystemMessage(
                content=DECISION_TOOL_USAGE_PROMPT.format(LLM_GUARDRAIL=LLM_GUARDRAIL)
            )
        ]
    memory = memory_store[session_id]

    memory.messages.append(HumanMessage(content=user_input))

    config = {"configurable": {"thread_id": session_id}}

    agent = await TravelPlannerAgent().get_main_agent()

    async def _event_generator():
        try:
            async for chunk in agent.astream(
                {"messages": memory.messages},  # 전체 대화 히스토리 전달
                stream_mode="messages",
                config=config,
            ):
                yield ServerSentEvent(
                    data=json.dumps(chunk[0].content), event="message"
                )
            yield ServerSentEvent(data=json.dumps(chunk[0].content), event="end")
        except Exception as e:
            yield ServerSentEvent(data=json.dumps({"error": str(e)}), event="error")

    return EventSourceResponse(_event_generator())
