from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from repository.MusicRepository import MusicRepository
from services.LLMBase import BaseForLLM
from services.LLMSanitizer import SQLSanitizer
from services.LLMTools import handle_tool_errors, executeQuery, ToolCallSanitizer


class OllamaService(BaseForLLM):

    def __init__(self, repo: MusicRepository, sanitizer: SQLSanitizer):
        super().__init__(sanitizer)

        self.repo = repo
        model = ChatOllama(model = "qwen3.5:latest", reasoning= True)
        self.chatModel = create_agent(
        model = model,
        middleware= [handle_tool_errors],
        tools= [executeQuery],
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
        async for chunk in llm.astream(
                {"messages": [HumanMessage(f"{message}")]},
                        stream_mode = "values",
                        config={"configurable": {"repository": self.repo},
                                "callbacks": [ToolCallSanitizer()]
                               }):
            for key, value in chunk.items():
                msg = value[-1]
                conversation.append(msg)
                msg.pretty_print()

        return conversation[-1]
