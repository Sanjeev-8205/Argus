from langgraph.graph import StateGraph

from app.agent.state import AgentState


def build_agent():
    agent_builder = StateGraph(AgentState)

    return agent_builder