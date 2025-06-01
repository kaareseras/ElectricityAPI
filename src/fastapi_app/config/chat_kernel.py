from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
)

from src.fastapi_app.config.config import get_settings

settings = get_settings()
deployment_name = settings.AZURE_OPENAI_DEPLOYMENT
endpoint = settings.AZURE_OPENAI_ENDPOINT
api_key = settings.AZURE_OPENAI_KEY


def get_kernel() -> tuple[Kernel, AzureChatCompletion]:
    kernel = Kernel()
    service_id = "AZURE_OPENAI"
    chat_service = AzureChatCompletion(
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key,
        service_id=service_id,
        instruction_role=None,
    )
    settings = AzureChatPromptExecutionSettings(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    kernel.add_service(chat_service)
    return kernel, chat_service, settings
