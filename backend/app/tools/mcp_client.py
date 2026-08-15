from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(
    command="uv",
    args=[
        "run",
        "mcp",
        "run",
        "app/tools/retrieval.py"
    ]
)

class MCPClient:
    def __init__(self):
        self._exit_stack = AsyncExitStack()
        self.session: ClientSession | None=None

    async def __aenter__(self):
        read, write = await self._exit_stack.enter_async_context(
            stdio_client(SERVER_PARAMS)
        )

        self.session = await self._exit_stack.enter_async_context(
            ClientSession(read, write)
        )

        await self.session.initialize()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.session=None
        await self._exit_stack.aclose()
        
    async def tool_list(self) -> list[dict[str, Any]]:
        if self.session is None:
            raise RuntimeError("MCP client is not connected")

        print("Calling MCP tools")
        tools = await self.session.list_tools()
        print("MCP tools list retrieved")

        return [
            {
                "name": tool.name,
                "description": tool.description,
                "schema": tool.input_schema
            }
            for tool in tools.tools
        ]
        
    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> object:
        if self.session is None:
            raise RuntimeError("MCP client is not connected")

        print("Before session.call_tool()")
        result = await self.session.call_tool(
            tool_name,
            arguments
        )
        print("After session.call_tool()")

        if result.is_error:
            raise RuntimeError(
                f"MCP tool {tool_name} failed: {result}"
            )

        if result.structured_content is not None:
            return result.structured_content

        return result.content