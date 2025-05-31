from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPSsePlugin
from semantic_kernel.contents.chat_history import ChatHistory

from src.fastapi_app.config.chat_kernel import create_default_agent, get_kernel

kernel = get_kernel()

copilot_router = APIRouter(
    prefix="/copilot",
    tags=["Copilot"],
    responses={404: {"description": "Not found"}},
)


class ChatRequest(BaseModel):
    message: str


@copilot_router.post("/chat/")
async def chat(request: ChatRequest):
    try:
        # Retrieve the chat completion service by type
        chat_service = kernel.get_service(type=ChatCompletionClientBase)

        chat_history = ChatHistory()

        chat_history.add_system_message("You are a helpful assistant.")
        chat_history.add_user_message(request.message)

        execution_settings = OpenAIChatPromptExecutionSettings()
        execution_settings.temperature = 0.7  # Adjust temperature for response variability
        execution_settings.stream = False  # Limit the response length

        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings,
        )

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@copilot_router.post("/agent/")
async def agent(request: ChatRequest):
    chat_history: ChatHistory = ChatHistory()
    thread: ChatHistoryAgentThread = ChatHistoryAgentThread()

    chat_history.add_system_message("You are a helpful assistant.")
    chat_history.add_user_message(request.message)

    async with MCPSsePlugin(
        name="prices",
        description="get danish electricity tax prices",
        url="http://localhost:8000/get-taxes-mcp",
    ) as price_plugin:
        agent: ChatCompletionAgent = create_default_agent(
            agent_name="prices-agent",
            model_name="gpt-4.1-nano",
            instructions="Answer questions about get danish electricity tax prices. use tools provided",
            plugins=[price_plugin],
        )

        responses = []
        async for message in agent.invoke(messages=chat_history, thread=thread):
            responses.append(message)

        final_response = responses[-1] if responses else None

        # Extract just the assistant's reply text
        return {"response": final_response.content if final_response else "No response"}
