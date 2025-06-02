from datetime import datetime

import pytz
from fastapi import HTTPException
from semantic_kernel.connectors.mcp import MCPSsePlugin
from semantic_kernel.contents.chat_history import ChatHistory

from src.fastapi_app.config.chat_kernel import get_kernel
from src.fastapi_app.config.config import get_settings
from src.fastapi_app.responses.copilot import ChatResponse
from src.fastapi_app.schemas.copilot import ChatHistoryElement, ChatRequest

config = get_settings()
deployment_name = config.AZURE_OPENAI_DEPLOYMENT
endpoint = config.AZURE_OPENAI_ENDPOINT
api_key = config.AZURE_OPENAI_KEY
mcp_url = config.BACKEND_HOST + "/" + config.MCP_ROUTE

kernel = get_kernel()


def parse_chat_history(chat_history: ChatHistory, history: list[ChatHistoryElement]) -> ChatHistory:
    for entry in history:
        if entry.role == "user":
            chat_history.add_user_message(entry.content)
        elif entry.role == "assistant":
            chat_history.add_assistant_message(entry.content)
    return chat_history


async def get_chat_response(request: ChatRequest):
    dk_timezone = pytz.timezone("Europe/Copenhagen")
    dk_time = datetime.now(dk_timezone).isoformat()

    system_message = f"""
        You are a chat bot. And you help users interact with prices on electricity in denmark.
        You are especially good at answering questions about the taxes and tarifs and current price.
        You can call functions to get the information you need.
        current time is {dk_time}
        When quering for spotprices, always use 'DK1' or 'DK2' as area, depending on the user location.
        'DK1' is the western part of denmark including fyn, and 'DK2' is the eastern part of denmark.
        If your missing information to answer a question, ask the user to provide the information.
        If you don't know the answer, say that you don't know.
        Answer in Danish exept if the user is asking in a different language, then answer in that language.
        Limit the data gathered to maximum of 5 day for spotprices.
        Spotprices are only available from 1/4 2025 days and current day.
        Spotprices is avialable for tomorrow if the time is after 2pm today.
        """
    kernel, chat_service, settings = get_kernel()

    chat_history = ChatHistory()
    chat_history.add_system_message(system_message)
    chat_history.add_user_message(request.message)
    history = parse_chat_history(chat_history, request.history)

    async with MCPSsePlugin(
        name="prices",
        description="get danish electricity tax prices and spotprices",
        url=mcp_url,
    ) as price_plugin:
        kernel.add_plugin(price_plugin)
        result = await chat_service.get_chat_message_content(history, settings, kernel=kernel)
        if not result.items:
            raise HTTPException(status_code=404, detail="No response from the chat service.")
        response = ChatResponse(
            content=result.items[0].text,
        )
        return response
