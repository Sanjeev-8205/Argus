from unittest.mock import MagicMock

from app.agent.nodes import answer_node


def test_answer_node():
    llm = MagicMock()

    llm.invoke.return_value.content = (
        "1. Employees must maintain confidentiality of company information and customer data."
        "2. Employees are expected to act professionally, ethically, and in compliance with all applicable laws and company policies."
    )

    state = {
        "query": "What is the remote work policy?",
        "plan": "Retrieve the remote work policy and use it to answer.",
        "tool_call": {
            "name": "retrieve_documents",
            "arguments": "What is the remote work policy?"
        },
        "tool_history": [
            {
                "name": "retrieve_documents",
                "arguments": "What is the remote work policy?"
            }
        ],
        "observation": {
            "result": [
                {
                    "document_id": "company_policy",
                    "chunk_id": "company_policy_0",
                    "text": "company policies..."
                }
            ]
        },
        "observation_history": [
            {
                "result": [
                    {
                        "document_id": "company_policy",
                        "chunk_id": "company_policy_0",
                        "text": "company policies..."
                    }
                ]
            }
        ],
        "retrieved_context": "",
        "messages": [],
        "final_answer": "",
        "step_count": 1,
        "max_steps": 5,
        "should_continue": False,
    }


    result = answer_node(state, llm)

    assert result["final_answer"] is not None
    assert "compliance" in result["final_answer"]