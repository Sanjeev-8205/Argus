import asyncio

from app.agent.graph import agent
from app.agent.llm import get_llm
from app.tools.mcp_client import MCPClient


async def main():
    llm = get_llm()

    async with MCPClient() as client:

        available_tools = await client.tool_list()

        agent_ = await agent(llm, client, available_tools)
        state = {
            "query": "What are the company's remote work expectations and leave policy?",
            "plan": "",
            "tool_call": None,
            "tool_history": [],
            "observation": None,
            "observation_history": [],
            "retrieved_context": "",
            "messages": [],
            "final_answer": "",
            "step_count": 0,
            "max_steps": 5,
            "should_continue": False,
        }

        result = await (agent_).ainvoke(state)

        print("\nFINAL STATE")
        print("=" * 60)

        print("Plan:")
        print(result["plan"])

        print("\nTool call:")
        print(result["tool_call"])

        print("\nObservation:")
        print(result["observation"])

        print("\nFinal answer:")
        print(result["final_answer"])

        print("\nStep count:")
        print(result["step_count"])

if __name__ == "__main__":
    asyncio.run(main())