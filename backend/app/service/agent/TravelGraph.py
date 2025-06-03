from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Optional, List
from pydantic import BaseModel
from enum import StrEnum
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_tavily import TavilySearch
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from core.config import env
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class EnumCompanion(StrEnum):
    ALONE = "혼자"
    COUPLE = "연인과 함께"
    FAMILY = "가족과 함께"
    FRIENDS = "친구들과 함께"

class ChatState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    need_user_input: bool = False
    companion: Optional[EnumCompanion] = None
    location: Optional[str] = None
    period: Optional[str] = None
    budget: Optional[str] = None
    travel_type: Optional[str] = None

class TravelPreferences(BaseModel):
    purpose: str
    travel_type: str
    travel_style: str
    travel_theme: str

class TravelGraph:
    def __init__(self):
        ...

    """
    Main Nodes
    """

    @staticmethod
    async def classification_intention(state: ChatState):
        from app.service.agent.prompt.tool.decision_tool_usage import PROMPT as DECISION_TOOL_USAGE_PROMPT

        llm = init_chat_model(
            model=f"{env.LLM_PROVIDER}:{env.LLM_MODEL}",
            temperature=0.7,
            streaming=True,
        )

        response = await llm.ainvoke(state.messages)
        return ChatState(messages=[*state.messages, response])

    """
    Tools
    """
    def build_graph(self):
        graph_builder = StateGraph(ChatState)
        graph_builder.add_node("chatbot", self.classification_intention)

        graph_builder.add_edge(START, "chatbot")

        checkpointer = MemorySaver()
        return graph_builder.compile(checkpointer=checkpointer)

    def _image_graph(self):
        graph = self.build_graph()
        graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
