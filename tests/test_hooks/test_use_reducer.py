from unittest.mock import Mock

from pyhooks.reducers import use_reducer


def test_simple_state_mutation():
    def tasks_reducer(current_state, action):
        if action["type"] == "ADD_TASK":
            return {"tasks": current_state["tasks"] + [action["task"]]}
        return current_state

    state, dispatch = use_reducer(tasks_reducer, {"tasks": []})
    new_state = dispatch({"type": "ADD_TASK", "task": "Do the dishes"})

    assert state == {"tasks": []}, "The original state should not be mutated"
    assert new_state == {"tasks": ["Do the dishes"]}, "The new state should be mutated"


def test_simple_middleware():
    mock = Mock()

    def logging_middleware(state, next, action):
        mock()
        new_state = next(state, action)
        mock()
        return new_state

    def tasks_reducer(current_state, action):
        if action["type"] == "ADD_TASK":
            return {"tasks": current_state["tasks"] + [action["task"]]}
        return current_state

    state, dispatch = use_reducer(tasks_reducer, {"tasks": []}, [logging_middleware])

    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})

    assert mock.call_count == 2
