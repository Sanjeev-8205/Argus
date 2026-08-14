from app.agent.graph import agent, route_after_reflect


def test_agent_graph():
    assert agent is not None

def test_route_after_reflect_continues():
    state = {
        "should_continue": True
    }

    assert route_after_reflect(state) == 'plan'

def test_route_after_reflect_answers():
    state = {
        "should_continue": False
    }

    assert route_after_reflect(state) == "answer"