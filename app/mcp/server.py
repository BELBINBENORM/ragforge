from mcp.server.mcpserver import MCPServer

from app.mcp.tools import register_conversation_tool, register_search_tool

mcp = MCPServer("RAGForge Server", 
              "0.1.0", 
              "RAGForge MCP Server for RAGForge Platform")


register_search_tool(mcp)
register_conversation_tool(mcp)

if __name__ == "__main__":
    mcp.run()