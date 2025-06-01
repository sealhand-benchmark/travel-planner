from pydantic import BaseModel
from datetime import datetime


class ResponsePostChatInitConfig(BaseModel):
    session_id: str
    session_created_at: datetime
