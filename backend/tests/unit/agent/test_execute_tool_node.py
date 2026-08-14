from unittest.mock import AsyncMock, patch

import pytest

from app.agent.nodes import execute_tool_node


@pytest.mark.asyncio
async def test_execute_tool_node():
    state = {
        "query": "What is the remote work policy?",
        "plan": "Retrieve the remote work policy and use it to answer.",
        "tool_call": {"name": "retrieve_documents", "arguments":{"query": "What is the remote work policy?"}},
        "observation": None,
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

    assert result["tool_call"]["name"] == "retrieve_documents"
    assert result["observation"] == retrieval_result
    assert result["step_count"] == 1

@pytest.mark.asyncio
async def test_execute_tool_node_raises_error_without_tools():
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
        await execute_tool_node(state)