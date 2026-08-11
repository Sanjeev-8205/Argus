from typing import TypedDict


class AgentState(TypedDict):
    query: str

    plan: str

    tool_name: str
    tool_input: str
    observation: str

    retrieved_context: str

    messages: list[str]

    final_answer: str

    step_count: int
    max_steps: int
    should_continue: bool