import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Query, Request, Path
import uuid
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from api.schema.chat import ResponsePostChatInitConfig
from langgraph.checkpoint.memory import MemorySaver
from app.service.agent.test import build_graph
from langgraph.prebuilt import create_react_agent
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.service.agent.prompt.tool.decision_tool_usage import (
    PROMPT as DECISION_TOOL_USAGE_PROMPT,
)
from app.service.agent.prompt.common._llm_guardrail import LLM_GUARDRAIL
from core.config import SESSION_MEMORIES
from fastapi.middleware.cors import CORSMiddleware


chat_router = APIRouter()

from app.service.agent.TravelGraph import TravelGraph

graph = TravelGraph().build_graph()

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


@chat_router.get(
    path="/response/{session_id}",
    summary="응답 요청",
    description="응답 요청",
)
async def chat(
    request: Request,
    session_id: str = Path(...),
    user_input: str = Query(...),
):
    try:
        if session_id not in SESSION_MEMORIES:
            SESSION_MEMORIES[session_id] = MemorySaver()

        graph_config = {"configurable": {"thread_id": session_id}}

        async def _event_generator():
            try:
                async for event in graph.astream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=graph_config,
                    stream_mode="messages",
                ):
                    if isinstance(event[0], AIMessage):
                        if getattr(event[0], "content", None):
                            yield ServerSentEvent(
                                data=json.dumps({"message": event[0].content}), event="message"
                            )
            except Exception as e:
                raise e
                # yield ServerSentEvent(data=json.dumps({"error": str(e)}), event="error")
                # return

        return EventSourceResponse(_event_generator())
    except Exception as e:
        raise e
