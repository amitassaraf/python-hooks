The Redux plugin is a state management plugin that provides a familiar API for Redux users.

It provides one global store that can be used by any function to get and set state.

### Installation

```bash
pip install python-hooks[redux]
```

### Usage

```python
from hooks import combine_reducers
from hooks.plugins.redux import create_redux_store, use_dispatch, use_selector


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
    print(use_selector(lambda state: state.tasks))      # Output: []
    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})
    print(use_selector(lambda state: state.tasks))      # Output: ["Do the dishes"]
```
