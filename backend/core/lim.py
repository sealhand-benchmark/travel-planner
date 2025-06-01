from enum import StrEnum
from functools import partial
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

__all__ = ["llm_dict", "LLMAPIModel"]


class LLMAPIModel(StrEnum):
    openai_gpt4o = "gpt-4o"
    openai_gpt4o_mini = "gpt-4o-mini"
    openai_gpt4dot1 = "gpt4.1"
    gemini_flash_2dot5 = "gemini-2.5-flash"
    gemini_pro_2dot5 = "gemini-2.5-pro"


llm_dict = {
    LLMAPIModel.openai_gpt4o: partial(ChatOpenAI, model="gpt-4o"),
    LLMAPIModel.openai_gpt4o_mini: partial(ChatOpenAI, model="gpt-4o-mini"),
    LLMAPIModel.openai_gpt4dot1: partial(ChatOpenAI, model="gpt4.1"),
    LLMAPIModel.gemini_flash_2dot5: partial(
        ChatGoogleGenerativeAI, model="gemini-2.5-flash"
    ),
    LLMAPIModel.gemini_pro_2dot5: partial(
        ChatGoogleGenerativeAI, model="gemini-2.5-pro"
    ),
}
