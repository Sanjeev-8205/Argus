from unittest.mock import AsyncMock, patch

import pytest

from app.agent.nodes import execute_tool_node


@pytest.mark.asyncio
async def test_execute_tool_node():
    state = {
        "query": "What is the remote work policy?",
        "plan": "Retrieve the remote work policy and use it to answer.",
        "tool_call": {"name": "retrieve_documents", "arguments":{"query": "What is the remote work policy?"}},
        "tool_history": [],
        "observation": None,
        "observation_history": [],
        "retrieved_context": "",
        "messages": [],
        "final_answer": "",
        "step_count": 0,
        "max_steps": 5,
        "should_continue": False,
    }

    retrieval_result = {
        "result": [
            {
                "document_id": "company_policy",
                "chunk_id": "company_policy_4",
                "text": "Remote work expectations...",
                "score": 0.9,
            }
        ]
    }

    with patch("app.agent.nodes.call_tool", new=AsyncMock(return_value=retrieval_result)) as mock_call:

        result = await execute_tool_node(state)

    mock_call.assert_awaited_once_with(
        tool_name="retrieve_documents",
        arguments={"query": "What is the remote work policy?"}
    )

    assert result["step_count"] == 1

    assert result["tool_call"]["name"] == "retrieve_documents"
    assert len(result["tool_history"]) == 1
    assert result["tool_history"][0] == state["tool_call"]

    assert result["observation"] == retrieval_result
    assert len(result["observation_history"]) == 1
    assert result["observation_history"][0] == retrieval_result

@pytest.mark.asyncio
async def test_execute_tool_node_with_two_tool_calls():

    tool_call_1 = {
        "name": "retrieve_documents",
        "arguments": {
            "query": "What is the remote work policy?"
        },
    }

    tool_call_2 = {
        "name": "retrieve_documents",
        "arguments": {
            "query": "What is the remote attendance policy?"
        },
    }

    retrieval_result_1 = {
        "result": [
            {
                "document_id": "company_policy",
                "chunk_id": "company_policy_4",
                "text": "Remote work expectations...",
                "score": 0.9,
            }
        ]
    }

    retrieval_result_2 = {
        "result": [
            {
                "document_id": "attendance_policy",
                "chunk_id": "attendance_policy_3",
                "text": "Attendance expectations for remote workers...",
                "score": 0.9,
            }
        ]
    }

    state_1 = {
        "query": "What are the company's remote work and attendance policies?",
        "plan": "Retrieve the remote work policy.",
        "tool_call": tool_call_1,
        "tool_history": [],
        "observation": None,
        "observation_history": [],
        "retrieved_context": "",
        "messages": [],
        "final_answer": "",
        "step_count": 0,
        "max_steps": 5,
        "should_continue": False,
    }

    state_2 = {
        **state_1,
        "plan": "Retrieve the remote attendance policy.",
        "tool_call": tool_call_2,
        "tool_history": [],
        "observation": None,
        "observation_history": [],
        "step_count": 0,
    }

    mock_call = AsyncMock(
        side_effect=[
            retrieval_result_1,
            retrieval_result_2,
        ]
    )

    with patch(
        "app.agent.nodes.call_tool",
        new=mock_call,
    ):

        result_1 = await execute_tool_node(state_1)

        state_2 = {
            **state_2,
            "tool_history": result_1["tool_history"],
            "observation_history": result_1["observation_history"],
            "step_count": result_1["step_count"],
        }

        result_2 = await execute_tool_node(state_2)

    # First MCP call
    mock_call.assert_any_await(
        tool_name="retrieve_documents",
        arguments={
            "query": "What is the remote work policy?"
        },
    )

    # Second MCP call
    mock_call.assert_any_await(
        tool_name="retrieve_documents",
        arguments={
            "query": "What is the remote attendance policy?"
        },
    )

    assert mock_call.await_count == 2

    # Execution state
    assert result_2["step_count"] == 2

    # Current tool call
    assert result_2["tool_call"] == tool_call_2

    # Tool history
    assert result_2["tool_history"] == [
        tool_call_1,
        tool_call_2,
    ]

    # Current observation
    assert result_2["observation"] == retrieval_result_2

    # Observation history
    assert result_2["observation_history"] == [
        retrieval_result_1,
        retrieval_result_2,
    ]

@pytest.mark.asyncio
async def test_execute_tool_node_raises_error_without_tools():
    state = {
            "query": "What is the remote work policy?",
            "plan": "Retrieve the remote work policy and use it to answer.",
            "tool_call": None,
            "tool_history": [],
            "observation": None,
            "observation_history": [],
            "retrieved_context": "",
            "messages": [],
            "final_answer": "",
            "step_count": 0,
            "max_steps": 5,
            "should_continue": False,
        }

    with pytest.raises(RuntimeError):
        await execute_tool_node(state)