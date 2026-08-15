import asyncio

from app.tools.mcp_client import MCPClient


async def test_mcp_client():
    async with MCPClient() as client:
        print("Retrieving Tools...")
        tools = await client.tool_list()
        print(tools)

        print("Retrieving Results...")
        result = await client.call_tool(
            tool_name="retrieve_documents",
            arguments={"query": "What is the company leave policy?"}
        )

        print(result)

if __name__ == "__main__":
    asyncio.run(test_mcp_client())