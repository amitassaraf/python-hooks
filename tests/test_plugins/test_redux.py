from hooks import combine_reducers
from hooks.plugins.redux import set_redux_store, use_dispatch, use_selector


def tasks_reducer(current_state: dict, action: dict) -> dict:
    if action["type"] == "ADD_TASK":
        return {"tasks": current_state["tasks"] + [action["task"]]}
    return current_state


def user_reducer(current_state: dict, action: dict) -> dict:
    if action["type"] == "SET_USER":
        return {"user": action["user"]}
    return current_state


combined_reducer = combine_reducers(tasks_reducer, user_reducer)
set_redux_store(combined_reducer, {"tasks": [], "user": None})


def test_basic_get_and_set() -> None:
    dispatch = use_dispatch()
    assert use_selector(lambda state: state.tasks) == []
    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})
    assert use_selector(lambda state: state.tasks) == ["Do the dishes"]
