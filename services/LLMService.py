from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from repository.MusicRepository import MusicRepository
from services.LLMTools import handle_tool_errors, executeQuery


class LLMService:

    def __init__(self, repo : MusicRepository):
        self.repo = repo
        model = ChatOllama(model = "qwen2.5")
        self.chatModel = create_agent(
        model = model,
        middleware= [handle_tool_errors],
        tools= [executeQuery],
        system_prompt= """
            You are an assistant named Mario. You have full access to the database and can perform any 
            query. In case of error, use the tool to run queries to study the structure of the
            tables. Do not ask the user for any permission; provide an answer to the user question as soon as you can"""
        )
        
    async def sendMessage(self, message : str):
        llm = self.chatModel
        async for chunk in llm.astream({"messages": [HumanMessage(f"{message}")]},config={"configurable": {"repository": self.repo}}):
            for key, value in chunk.items():
                for msg in value["messages"]:
                    msg.pretty_print()
                    yield msg