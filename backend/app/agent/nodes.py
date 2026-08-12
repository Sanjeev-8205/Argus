from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.state import AgentState

PLANNER_SYSTEM_PROMPT = """You are the planning component of Argus.

Your job is to create a concise execution plan for the user's request.

Determine:
1. What information is required.
2. Which tool or tools may be required.
3. The order in which those tools should be used.
4. When enough information will be available to answer.

Do not answer the user's question.
Do not execute tools.
Return only the execution plan.
"""

ACT_SYSTEM_PROMPT = """You are the action-selection component of Argus.

Given the user's request and the current execution plan, determine the next
tool that should be called.

Return:
- the tool name
- the arguments required by that tool

Do not execute the tool yourself.
"""

def plan_node(state: AgentState, llm) -> AgentState:

    response = llm.invoke(
        [
            SystemMessage(
                content=PLANNER_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=f"User Query: {state["query"]}"
            )
        ]
    )

    return {
        **state,
        "plan": response.content,
        "step_count": state.get("step_count", 0)
    }
    
def act_node(state: AgentState, llm) -> AgentState:

    response = llm.invoke(
        [
            SystemMessage(
                content=ACT_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=(
                    f"User request:\n{state['query']}\n\n"
                    f"Execution plan:\n{state['plan']}"
                )
            )
        ]
    )

    return {
        **state,
        "observation": response.content
    }
    
def policy_gateway_node(state: AgentState) -> AgentState:
    raise NotImplementedError

def reflect_node(state: AgentState) -> AgentState:
    raise NotImplementedError

def answer_node(state: AgentState) -> AgentState:
    raise NotImplementedError