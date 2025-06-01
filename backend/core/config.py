from pydantic_settings import BaseSettings
from typing import Dict
from langchain.memory import ConversationBufferMemory


class Settings(BaseSettings):
    # 현재 LLM API 모델 설정
    LLM_PROVIDER: str
    LLM_MODEL: str
    # Lagnfuse
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_HOST: str

    # LLM API KEY
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str

    # KAKAO API KEY
    KAKAO_API_REST_KEY: str
    KAKAO_API_JS_KEY: str
    KAKAO_API_ADMIN_KEY: str
    KAKAO_REDIRECT_URI: str
    KAKAO_CLIENT_SECRET: str

    # POSTGRES
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    # REDIS
    REDIS_HOST: str = "redis://redis:6379"

    class Config:
        env_file = "../.env"


env = Settings()

# 세션별 메모리 저장소

SESSION_MEMORIES: Dict[str, ConversationBufferMemory] = (
    {}
)  # 대화내역은 현재 DB에 저장하지 않고 서비스 구동 중 저장으로 갈음합니다.
