from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.kernel import KernelArguments

from src.fastapi_app.config.config import get_settings

settings = get_settings()
deployment_name = settings.AZURE_OPENAI_DEPLOYMENT
endpoint = settings.AZURE_OPENAI_ENDPOINT
api_key = settings.AZURE_OPENAI_KEY


def get_kernel():
    kernel = Kernel()
    chat_completion_service = AzureChatCompletion(deployment_name=deployment_name, endpoint=endpoint, api_key=api_key)
    kernel.add_service(chat_completion_service)
    return kernel


def create_default_agent(agent_name: str, model_name: str, instructions: str = None, plugins: list = None):
    """Create a simple chat completion agent."""
    kernel = get_kernel()
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="myAgent",
        instructions="You are a helpful assistant use tools to answer questions.",
        plugins=[],
        arguments=KernelArguments(request_settings=request_settings()),
    )
    return agent


@staticmethod
def request_settings() -> OpenAIChatPromptExecutionSettings:
    """Create request settings for the OpenAI service."""
    return OpenAIChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
        max_tokens=1000,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
