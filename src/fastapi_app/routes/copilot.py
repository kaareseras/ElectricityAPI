from fastapi import APIRouter, status

from src.fastapi_app.responses.copilot import ChatResponse
from src.fastapi_app.schemas.copilot import ChatRequest
from src.fastapi_app.services.copilot import get_chat_response

copilot_router = APIRouter(
    prefix="/copilot",
    tags=["Copilot"],
    responses={404: {"description": "Not found"}},
)


@copilot_router.post("/agent/", status_code=status.HTTP_200_OK, response_model=ChatResponse)
async def agent(request: ChatRequest):
    response = await get_chat_response(request)
    return response
