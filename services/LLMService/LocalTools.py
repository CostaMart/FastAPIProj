import logging
import re

import sqlparse
from langchain.agents.middleware import wrap_tool_call
from langchain.tools import tool
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from repository.MusicRepository import MusicRepository


@tool
async def executeQuery(sqlQuery : str, config : RunnableConfig):
    """
    grant access to an sql lite DB containing Album and Artist tables

    Args:
        sqlQuery (str): sql lite query to execute in the form of a string """

    repository: MusicRepository = config["configurable"]["repository"]
    result = await repository.executeFreeQuery(sqlQuery)
    if len(result) == 0:
        return "retrieved empty list, ensure this is not an error"
    else:
        return result

@wrap_tool_call
async def handle_tool_errors(request, handler):
    try:
        return await handler(request)
    except Exception as e:
        return ToolMessage(
            content=(
                f"tool '{request.tool_call['name']}' failed with error: {str(e)}. "
                f"please try again and correct the error."
            ),
            tool_call_id=request.tool_call["id"]
        )



logger = logging.getLogger(__name__)
class ToolCallSanitizer(BaseCallbackHandler):
    """
        NOTE: this would not be necessary in a real environment.
        Instead of limiting the kind of queries the model can run we can just assign a user with not write privileges
        in the database
     """

    raise_error = True
    def on_tool_start(self, serialized, input_str, **kwargs):
        query = extract_query(input_str)

        if query is None:
            return

        if containsReadQuery(query):
            print("tool call permitted")
            return
        else:
            raise Exception("only read query are permitted")

def containsReadQuery(query:str) -> bool :
    parsed = sqlparse.parse(query)[0]
    type = parsed.get_type()
    return type == "SELECT"

def extract_query(s: str) -> str | None:
    match = re.search(r"'sqlQuery':\s*[\"'](.+?)[\"']}", s)
    return match.group(1) if match else None
