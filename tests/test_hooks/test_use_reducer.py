# mypy: ignore-errors

from typing import Any, Callable

from unittest.mock import Mock

from hooks.reducers import combine_reducers, use_reducer


def test_simple_state_mutation() -> None:
    def tasks_reducer(
        current_state: dict[str, Any], action: dict[str, Any]
    ) -> dict[str, Any]:
        if action["type"] == "ADD_TASK":
            return {"tasks": current_state["tasks"] + [action["task"]]}
        return current_state

    state, dispatch = use_reducer(tasks_reducer, {"tasks": []})
    new_state = dispatch({"type": "ADD_TASK", "task": "Do the dishes"})

    assert state == {"tasks": []}, "The original state should not be mutated"
    assert new_state == {"tasks": ["Do the dishes"]}, "The new state should be mutated"


def test_simple_middleware() -> None:
    mock = Mock()

    def logging_middleware(
        state: dict[str, Any], next: Callable[[Any, Any], Any], action: dict[str, Any]
    ) -> dict[str, Any]:
        mock()
        new_state: dict[str, Any] = next(state, action)
        mock()
        return new_state

    def tasks_reducer(
        current_state: dict[str, Any], action: dict[str, Any]
    ) -> dict[str, Any]:
        if action["type"] == "ADD_TASK":
            return {"tasks": current_state["tasks"] + [action["task"]]}
        return current_state

    state, dispatch = use_reducer(tasks_reducer, {"tasks": []}, [logging_middleware])

    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})

    assert mock.call_count == 2


def test_simple_state_mutation_multiple_calls() -> None:
    def tasks_reducer(
        current_state: dict[str, Any], action: dict[str, Any]
    ) -> dict[str, Any]:
        if action["type"] == "ADD_TASK":
            return {"tasks": current_state["tasks"] + [action["task"]]}
        return current_state

    state, dispatch = use_reducer(tasks_reducer, {"tasks": []})

    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})

    # .... Other section in the program

    state, dispatch = use_reducer(tasks_reducer)

    assert state == {"tasks": ["Do the dishes"]}, "The new state should be mutated"


def test_combine_reducers() -> None:
    def tasks_reducer(current_state: dict, action: dict) -> dict:
        if action["type"] == "ADD_TASK":
            return {"tasks": current_state["tasks"] + [action["task"]]}
        return current_state

    def user_reducer(current_state: dict, action: dict) -> dict:
        if action["type"] == "SET_USER":
            return {"user": action["user"]}
        return current_state

    combined_reducer = combine_reducers(tasks_reducer, user_reducer)
    state, dispatch = use_reducer(combined_reducer, {"tasks": [], "user": None})

    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})
    dispatch({"type": "SET_USER", "user": "John Doe"})

    state, _ = use_reducer(combined_reducer)

    assert state == {
        "tasks": ["Do the dishes"],
        "user": "John Doe",
    }, "The new state should be mutated"
