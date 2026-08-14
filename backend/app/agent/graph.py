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
from app.agent.llm import get_llm

def route_after_reflect(state: AgentState) -> str:
    if state["should_continue"] is True:
        return "plan"
    
    return "answer"

def build_agent():
    llm = get_llm()

    agent_builder = StateGraph(AgentState)

    agent_builder.add_node("act", act_node)

    agent_builder.add_node(
        "plan",
        lambda state: plan_node(state, llm)
    )

    agent_builder.add_node("policy", policy_gateway_node)
    agent_builder.add_node("tool", execute_tool_node)
    agent_builder.add_node("reflect", reflect_node)
    
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

agent = build_agent()