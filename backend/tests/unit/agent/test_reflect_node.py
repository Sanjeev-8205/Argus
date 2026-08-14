from app.agent.nodes import reflect_node


def test_reflect_node():
    state = {
        "query": "What is the remote work policy?",
        "plan": "Retrieve the remote work policy and use it to answer.",
        "tool_call": {
            "name": "retrieve_documents",
            "arguments": "What is the remote work policy?"
        },
        "observation": {
            "result": [
                {
                    "document_id": "company_policy",
                    "chunk_id": "company_policy_0",
                    "text": "company policies..."
                }
            ]
        },
        "retrieved_context": "",
        "messages": [],
        "final_answer": "",
        "step_count": 0,
        "max_steps": 5,
        "should_continue": True,
    }

    result = reflect_node(state)

    assert result["should_continue"] is False


def test_reflect_node_returns_false_on_max_steps():
    state = {
        "query": "What is the remote work policy?",
        "plan": "Retrieve the remote work policy and use it to answer.",
        "tool_call": {
            "name": "retrieve_documents",
            "arguments": "What is the remote work policy?"
        },
        "observation": {"result": []},
        "retrieved_context": "",
        "messages": [],
        "final_answer": "",
        "step_count": 5,
        "max_steps": 5,
        "should_continue": True,
    }

    result = reflect_node(state)

    assert result["should_continue"]==False

