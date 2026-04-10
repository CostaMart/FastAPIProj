import logging

from mcp.server.fastmcp import FastMCP
import sqlite3

logger = logging.getLogger(__name__)

mcp = FastMCP("SQL-MCP", port = 8081)

@mcp.tool()
def musicDatabaseQuery(query: str):
    """runs a query to an sqlite database and returns the result

    Args:
        query (str): the query to run
    """
    conn = sqlite3.connect("/home/costantino/PyCharmMiscProject/FastAPIProj/test.db")
    querier = conn.cursor()
    result = querier.execute(query)
    return result.fetchall()



if __name__ == "__main__":
    logger.info("Starting FastMCP, ready to accept connections...")
    mcp.run(transport= "sse")
