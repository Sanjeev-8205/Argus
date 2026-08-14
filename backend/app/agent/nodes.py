from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.state import AgentState
from app.tools.mcp_client import call_tool

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

ANSWER_SYSTEM_PROMPT = """
You are a helpful assistant.
Answer the user's question using the retrieved information provided by the user.

Rules:
- Ground your answer in the retrieved information.
- Do not invent information that is not present in the retrieved information.
- If the retrieved information is insufficient, say so.
- Keep the answer concise.
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
    
def act_node(state: AgentState) -> AgentState:

    tool_call = {
        "name": "retrieve_documents",
        "arguments": {"query": state["query"]}
    }
    
    return {
        **state,
        "tool_call": tool_call
    }
    
def policy_gateway_node(state: AgentState) -> AgentState:
    tool_call = state.get("tool_call")

    if tool_call is None:
        raise RuntimeError("Policy gateway received no tool call")

    return {
        **state,
        "tool_call": tool_call
    }

async def execute_tool_node(state: AgentState) -> AgentState:
    tool_call = state["tool_call"]

    if tool_call is None:
        raise RuntimeError("No tool call to execute")

    result = await call_tool(
        tool_name=tool_call["name"],
        arguments=tool_call["arguments"]
    )

    return {
        **state,
        "observation": result,
        "step_count": state.get("step_count", 0)+1
    }

def reflect_node(state: AgentState) -> AgentState:
    step_count = state.get("step_count", 0)
    max_steps = state.get("max_steps", 5)

    if step_count>=max_steps:
        return{
            **state,
            "should_continue": False
        }

    observation = state.get("observation", None)
    if observation is None:
        return {
            **state,
            "should_continue": False
        }

    return {
        **state,
        "should_continue": False
    }


def answer_node(state: AgentState, llm) -> AgentState:

    prompt = [
        SystemMessage(content=ANSWER_SYSTEM_PROMPT),
        HumanMessage(content=f"""
User's query:
{state["query"]}

Observations:
{state["observation"]}""")
    ]

    answer = llm.invoke(prompt)

    return {
        **state,
        "final_answer": answer.content
    }