from typing import List

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_ollama import ChatOllama
from fastapi import Depends
from langchain.tools import tool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from repository.injectors import injectMusicRepository


@tool
def executeQuery(sqlQuery : str):
    """
    grant access to an sql DB containing Album and Artist tables

    Args:
        sqlQuery (str): sql query to execute in the form of a string """
    try:
        DATABASE_URL = "sqlite:///./test.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        session = sessionmaker(bind=engine)
        with session.begin() as db:
            result = db.execute(text(sqlQuery))
            toReturn = result.fetchall()
            if type(toReturn) == list:
                if len(list(toReturn)) == 0:
                    return (
                        f"an empty list was fecthed"
                    )
            return toReturn

    except Exception as e:
        # Non lanci l'eccezione — ritorni il messaggio di errore come stringa
        # Il modello lo legge nel ToolMessage e può riprovare
        return (
            f"error executing query: {str(e)}. "
            f"check column's and table's names, then try again."
        )

class LLMService:

    def __init__(self, repo):
        self.repo = repo
        model = ChatOllama(
        model = "qwen2.5"
        )
        self.chatModel = create_agent(
        model = model,
        tools= [executeQuery],
        system_prompt= """You are an assistant named Mario. You have full access to the database and can perform any 
        query you wish. In case of an error, you can use the tool to independently run queries to study the structure of the
          tables. Do not ask the user for any permission; provide an answer to the user question as soon as you can""")
        



    def sendMessage(self, message : str):
        llm = self.chatModel
        for chunk in llm.stream({"messages": [HumanMessage(f"{message}")]}):
            for key, value in chunk.items():
                for msg in value["messages"]:
                    msg.pretty_print()
                    yield msg




def injectLLMService(repo = Depends(injectMusicRepository)):
    return LLMService(repo)

