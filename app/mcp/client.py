from mcp import Client, StdioServerParameters

server = StdioServerParameters(
    command="python",
    args=["-m", "app.mcp.server"],
)

async def get_mcp_client():
    return Client(server,mode="legacy")