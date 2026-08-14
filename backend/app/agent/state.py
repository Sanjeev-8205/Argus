from typing import Any, TypedDict


class ToolCall(TypedDict):
    name: str
    arguments: dict[str, Any]

class AgentState(TypedDict):
    query: str

    plan: str

    tool_call: ToolCall | None
    tool_history: list[ToolCall]

    observation: Any
    observation_history: list[Any]

    retrieved_context: str

    messages: list[str]

    final_answer: str

    step_count: int
    max_steps: int
    should_continue: bool