from app.agent.nodes import act_node


def test_act_node():

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

    response = act_node(state)

    assert response["tool_call"] is not None
    assert response["tool_call"]["name"] == "retrieve_documents"
    assert response["tool_call"]["arguments"]["query"] == state["query"]
