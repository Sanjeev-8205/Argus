from unittest.mock import MagicMock

from app.agent.nodes import plan_node


def test_plan_node_generates_plan():

    llm = MagicMock()

    llm.invoke.return_value.content = (
        "1. Search the knowledge base for relevant documents."
        "2. Inspect the retrieved information."
        "3. Answer the user's question."
    )

    state = {
        "query": "What is the company's remote work policy?",
        "plan": "",
        "tool_name": "",
        "tool_input": "",
        "observation": "",
        "retrieved_content": "",
        "messages": [],
        "final_answer": "",
        "step_count": 0,
        "max_steps": 5,
        "should_continue": False
    }

    response = plan_node(state, llm)

    assert response["plan"]
    assert "knowledge base" in response["plan"]

    llm.invoke.assert_called_once()