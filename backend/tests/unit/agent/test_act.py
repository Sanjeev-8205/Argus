from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agent.nodes import act_node


@pytest.mark.asyncio
async def test_act_node():
    llm = MagicMock()

    llm.invoke.return_value.content = "retrieve_documents"

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

    result = [
        {
            "name": "retrieve_documents",
            "description": "Retrieve Documents...",
            "schema": {
                "field1": "...",
                "field2": "..."
            }
        }
    ]

    with patch("app.agent.nodes.tool_list", new=AsyncMock(return_value=result)) as mock_tool_list:
        response = await act_node(state, llm)

    mock_tool_list.assert_awaited_once()

    assert response["tool_call"] is not None
    assert response["tool_call"]["name"] == "retrieve_documents"
    assert response["tool_call"]["arguments"]["query"] == state["query"]
