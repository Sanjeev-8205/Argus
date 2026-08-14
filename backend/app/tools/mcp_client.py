import asyncio
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

async def tool_list() -> list[dict[str, Any]]:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

        return [
            {
                "name": tool.name,
                "description": tool.description,
                "schema": tool.input_schema
            }
            for tool in tools.tools
        ]
    
async def call_tool(tool_name, arguments: dict[str, Any]) -> object:
    async with stdio_client(SERVER_PARAMS) as (read, write):  # noqa: SIM117
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            available_tools = [tool.name for tool in tools.tools]

            if tool_name not in available_tools:
                raise RuntimeError(
                    "MCP server does not expose retrieve_documents"
                )

            result = await session.call_tool(
                "retrieve_documents",
                arguments=arguments
            )

            if result.is_error:
                raise RuntimeError(
                f"MCP retrieval failed: {result}"
            )

            if result.structured_content is not None:
                return result.structured_content

            return result.content

async def main() -> None:
    tools = await tool_list()

    print("Available MCP tools:")

    for tool in tools:
        print(f"\nName: {tool['name']}")
        print(f"Description: {tool['description']}")
        print(f"Input schema: {tool['input_schema']}")

if __name__ == "__main__":
    asyncio.run(main())