from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    act_node,
    answer_node,
    execute_tool_node,
    plan_node,
    policy_gateway_node,
    reflect_node,
)
from app.agent.state import AgentState


def route_after_reflect(state: AgentState) -> str:
    if state["should_continue"] is True:
        return "plan"
    
    return "answer"

async def build_agent(llm, mcp_client, available_tools):

    agent_builder = StateGraph(AgentState)

    agent_builder.add_node(
        "plan",
        lambda state: plan_node(state, llm)
    )

    async def act(state):
        return await act_node(state, llm, mcp_client, available_tools)
    
    agent_builder.add_node("act", act)

    agent_builder.add_node("policy", policy_gateway_node)

    async def execute_tool(state):
        return await execute_tool_node(state, mcp_client)
    
    agent_builder.add_node("tool", execute_tool)

    agent_builder.add_node(
        "reflect", 
        lambda state: reflect_node(state, llm)
    )
    
    agent_builder.add_node(
        "answer", 
        lambda state: answer_node(state, llm)
    )

    agent_builder.add_edge(START, "act")
    agent_builder.add_edge("act", "plan")
    agent_builder.add_edge("plan", "policy")
    agent_builder.add_edge("policy", "tool")
    agent_builder.add_edge("tool", "reflect")

    agent_builder.add_conditional_edges(
        "reflect",
        route_after_reflect,
        {
            "plan": "plan",
            "answer": "answer"
        }
    )

    agent_builder.add_edge("answer", END)

    return agent_builder.compile()

async def agent(llm, client, available_tools):
    agent = await build_agent(llm, client, available_tools)

    return agent