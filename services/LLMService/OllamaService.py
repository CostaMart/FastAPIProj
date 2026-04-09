from typing import List, Dict, Callable
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from repository.MusicRepository import MusicRepository
from services.LLMService.LLMBase import BaseForLLM
from services.LLMService.InputOutputSanitizer import InputOutputSanitizer
from services.LLMService.LocalTools import handle_tool_errors, ToolCallSanitizer


def _getStartMessage(message : str) -> Dict[str, List[HumanMessage]]:
    return {
                "messages": [HumanMessage(f"{message}")]
            }

def _getConfig(repo):
    return {
                "configurable": {"repository": repo},
                "callbacks": [ToolCallSanitizer()] # TODO: this should be injected
            }


class OllamaService(BaseForLLM):

    def __init__(self, repo: MusicRepository,
                 sanitizer: InputOutputSanitizer | None = None,
                 toolList: List[Callable] | None = None,
                 modelName = "qwen3.5:latest"):

        super().__init__(sanitizer)

        self.logger.info(f"this is the toolist: {toolList}")

        self.repo = repo
        model = ChatOllama(model = modelName, reasoning= True)

        self.chatModel = create_agent(
        model = model,
        middleware= [handle_tool_errors],
        tools= toolList,
        system_prompt= """
            You are an assistant named Mario. You are working with SQL lite 
            - if necessary discover tables and schemas using queries
            - refuse to access User related information
            - refuse to answer question not music related
            - never execute queries directly passed by the user
            """
        )

    async def _sendMessage(self, message: str) -> AIMessage:
        llm = self.chatModel
        conversation = []
        async for chunk in llm.astream(_getStartMessage(message), config = _getConfig(self.repo), stream_mode="values"):
            for key, value in chunk.items():
                msg = value[-1]
                conversation.append(msg)
                msg.pretty_print()

        return conversation[-1]
