Here is where things get interesting. The `use_reducer` hook is used to manage state in a functional way.
It is similar to the `use_state` hook but allows us to manage more complex state.

---

### Basic use

Using the `use_reducer` hook is very similar to reducer concepts in other frameworks. The hook takes in a reducer
function and an initial state.
Intern, the hook returns a tuple containing the current state and a dispatch function. The dispatch function is used to
dispatch actions to the reducer function.

```py
from hooks import use_reducer


def tasks_reducer(current_state: dict, action: dict) -> dict:
  if action["type"] == "ADD_TASK":
    return {"tasks": current_state["tasks"] + [action["task"]]}
  return current_state


state, dispatch = use_reducer(tasks_reducer, {"tasks": []})
new_state = dispatch({"type": "ADD_TASK", "task": "Do the dishes"})

print(state)  # Output: {"tasks": []}
print(new_state)  # Output: {"tasks": ["Do the dishes"]}
```

The dispatch function can be used to dispatch actions from anywhere in the application. This allows us to manage the state 
in a centralised location. In addition, the use_reducer hook can be used multiple times in the same application and 
even in the same function. It knows to identify the correct state to update based on the reducer function passed in.

### Next steps

Learn about scoping hooks with [hooks_scope](../scoping/hooks_scope.md) decorator.
