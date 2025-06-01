from src.fastapi_app.responses.base import BaseResponse


class ChatResponse(BaseResponse):
    assistant: str
