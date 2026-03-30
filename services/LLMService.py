from langchain_ollama import ChatOllama


class LLMService:

    def __init__(self):
     self.chatModel = ChatOllama(
         model = "qwen2.4-coder"

     )
