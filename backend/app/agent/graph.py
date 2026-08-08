from app.agent.state import AgentState

from langgraph.graph import StateGraph

def build_agent():
    agent_builder = StateGraph(AgentState)

    return agent_builder