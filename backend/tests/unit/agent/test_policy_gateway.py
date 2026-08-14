import pytest

from app.agent.nodes import policy_gateway_node


def test_policy_gateway_returns_tools():
    state = {
        "query": "What is the remote work policy?",
        "plan": "Retrieve the remote work policy and use it to answer.",
        "tool_call": {"name": "retrieve_documents", "arguments": {"query": "What is the remote work policy?"}},
        "observation": None,
        "retrieved_context": "",
        "messages": [],
        "final_answer": "",
        "step_count": 0,
        "max_steps": 5,
        "should_continue": False,
    }

    result = policy_gateway_node(state)

    assert result["tool_call"] is not None
    assert result["tool_call"]["name"] == "retrieve_documents"
    assert result["tool_call"]["arguments"]["query"] == state["query"]

def test_policy_gateway_raises_error_without_tools():
    state = {
            "query": "What is the remote work policy?",
            "plan": "Retrieve the remote work policy and use it to answer.",
            "tool_call": None,
            "observation": None,
            "retrieved_context": "",
            "messages": [],
            "final_answer": "",
            "step_count": 0,
            "max_steps": 5,
            "should_continue": False,
        }

    with pytest.raises(RuntimeError):
        policy_gateway_node(state)