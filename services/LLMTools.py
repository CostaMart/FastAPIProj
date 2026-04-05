from langchain.agents.middleware import wrap_tool_call
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig

from repository.MusicRepository import MusicRepository



@tool
async def executeQuery(sqlQuery : str, config : RunnableConfig):
    """
    grant access to an sql DB containing Album and Artist tables

    Args:
        sqlQuery (str): sql query to execute in the form of a string """

    repository: MusicRepository = config["configurable"]["repository"]
    result = await repository.executeFreeQuery(sqlQuery)
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
