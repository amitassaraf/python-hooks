from hooks import combine_reducers
from hooks.plugins.redux import create_redux_store, use_dispatch, use_selector
from hooks.plugins.redux_async import create_redux_store as create_async_redux_store
from hooks.plugins.redux_async import use_dispatch as use_async_dispatch
from hooks.plugins.redux_async import use_selector as use_async_selector


def tasks_reducer(current_state: dict, action: dict) -> dict:
    if action["type"] == "ADD_TASK":
        return {"tasks": current_state["tasks"] + [action["task"]]}
    return current_state


def user_reducer(current_state: dict, action: dict) -> dict:
    if action["type"] == "SET_USER":
        return {"user": action["user"]}
    return current_state


combined_reducer = combine_reducers(tasks_reducer, user_reducer)
create_redux_store(combined_reducer, {"tasks": [], "user": None})


def test_basic_get_and_set() -> None:
    dispatch = use_dispatch()
    assert use_selector(lambda state: state.tasks) == []
    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})
    assert use_selector(lambda state: state.tasks) == ["Do the dishes"]


async def test_basic_get_and_set_async(async_backend) -> None:
    await create_async_redux_store(combined_reducer, {"tasks": [], "user": None})

    dispatch = await use_async_dispatch()
    assert await use_async_selector(lambda state: state.tasks) == []
    await dispatch({"type": "ADD_TASK", "task": "Do the dishes"})
    assert await use_async_selector(lambda state: state.tasks) == ["Do the dishes"]
