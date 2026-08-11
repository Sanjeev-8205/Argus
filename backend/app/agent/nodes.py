from app.agent.state import AgentState


def plan_node(state: AgentState) -> AgentState:
    raise NotImplementedError

def act_node(state: AgentState) -> AgentState:
    raise NotImplementedError

def policy_gateway_node(state: AgentState) -> AgentState:
    raise NotImplementedError

def reflect_node(state: AgentState) -> AgentState:
    raise NotImplementedError

def answer_node(state: AgentState) -> AgentState:
    raise NotImplementedError