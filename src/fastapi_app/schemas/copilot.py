from pydantic import BaseModel


class ChatHistoryElement(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatHistoryElement] = []
