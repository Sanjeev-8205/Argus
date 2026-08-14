from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.prompts import (
    get_action_prompt,
    get_answer_prompt,
    get_planner_prompt,
    get_reflect_prompt,
)
from app.agent.state import AgentState
from app.tools.mcp_client import call_tool, tool_list


def plan_node(state: AgentState, llm) -> AgentState:
    history_context = ""

    for index, (tool_call, observation) in enumerate(
        zip(state["tool_history"], state["observation_history"], start=1)):

        history_context += f"""
Tool Call {index}:
{tool_call}

Observation {index}:
{observation}"""
    
    response = llm.invoke(
        [
            SystemMessage(
                content=get_planner_prompt()
            ),
            HumanMessage(
                content=f"""
User Query:
{state["query"]}

Previous execution history:
{history_context}"""
            )
        ]
    )

    return {
        **state,
        "plan": response.content,
        "step_count": state.get("step_count", 0)
    }
    
async def act_node(state: AgentState, llm) -> AgentState:
    history_context = ""

    for index, (tool_call, observation) in enumerate(
        zip(state["tool_history"], state["observation_history"])):

        history_context += f"""
Tool Call {index}:
{tool_call}

Observation {index}:
{observation}"""

    available_tools = await tool_list()
    tool_names = [tool["name"] for tool in available_tools]

    response = llm.invoke(
        [
            SystemMessage(content=get_action_prompt()),
            HumanMessage(content=f"""
Plan:
{state["plan"]}

Available Tools:
{available_tools}

Previous execution history:
{history_context}""")
        ]
    )

    if response.content.strip() not in tool_names:
        raise ValueError("LLM selected an unavailable tool.")

    tool_call = {
        "name": response.content,
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
        "tool_history": [
            *state.get("tool_history", []),
            tool_call
        ],
        "observation_history": [
            *state.get("observation_history", []),
            result
        ],
        "step_count": state.get("step_count", 0)+1
    }

def reflect_node(state: AgentState, llm) -> AgentState:
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

    next_step = llm.invoke(
        [
            SystemMessage(content=get_reflect_prompt()),
            HumanMessage(content=f"""
User's Query:
{state["query"]}

Plan:
{state["plan"]}

Tool Call History:
{state["tool_history"]}

Observation History:
{state["observation_history"]}""")
        ]
    )

    valid_responses = ["content", "answer"]
    if next_step.content.strip().lower() not in valid_responses:
        raise ValueError("LLM generated an invalid response.")

    if next_step.content.lower() == "continue":
        return {
            **state,
            "should_continue": True
        }

    else:
        return {
            **state,
            "should_continue": False
        }


def answer_node(state: AgentState, llm) -> AgentState:

    prompt = [
        SystemMessage(content=get_answer_prompt()),
        HumanMessage(content=f"""
User's query:
{state["query"]}

All Tool Calls:
{state["tool_history"]}

All Observations:
{state["observation_history"]}""")
    ]

    answer = llm.invoke(prompt)

    return {
        **state,
        "final_answer": answer.content
    }