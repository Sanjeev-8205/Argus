import asyncio

from app.agent.graph import agent


async def main():
    state = {
        "query": "What are the company's remote work expectations?",
        "plan": "",
        "tool_call": None,
        "observation": None,
        "retrieved_context": "",
        "messages": [],
        "final_answer": "",
        "step_count": 0,
        "max_steps": 5,
        "should_continue": False,
    }

    result = await agent.ainvoke(state)

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