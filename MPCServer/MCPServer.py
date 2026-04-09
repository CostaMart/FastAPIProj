import logging

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP("SQL-MCP", port = 8081)

@mcp.tool()
def secretHappyMessage():
    """Prints an happy message in the console"""

    print("Im happy and i know it Happy!!!")
    return "the happy secret message is: you are a good boy"

if __name__ == "__main__":
    logger.info("Starting FastMCP, ready to accept connections...")
    mcp.run(transport= "sse")
