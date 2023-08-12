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

The dispatch function can be used to dispatch actions from anywhere in the application. This allows us to manage the
state
in a centralised location. In addition, the use_reducer hook can be used multiple times in the same application and
even in the same function. It knows to identify the correct state to update based on the reducer function passed in.

---

### Accessing the state in separate functions

You may use the `use_reducer` hook in separate functions and still access the same state. This is because the hook
uses the same reducer function to identify the state to update. This is useful when you want to separate your logic
into different functions.

```python
from hooks import use_reducer


def tasks_reducer(current_state: dict, action: dict) -> dict:
  if action["type"] == "ADD_TASK":
    return {"tasks": current_state["tasks"] + [action["task"]]}
  return current_state


def add_task(task: str):
  state, dispatch = use_reducer(tasks_reducer, {"tasks": []})
  dispatch({"type": "ADD_TASK", "task": task})


def get_tasks():
  state, dispatch = use_reducer(tasks_reducer)
  return state["tasks"]


add_task("Do the dishes")
add_task("Do the laundry")
print(get_tasks())  # Output: ["Do the dishes", "Do the laundry"]
```

---
### Middleware

The `use_reducer` hook also supports middleware. Middleware is a function that is called before the reducer processes
the action. This allows you to perform actions such as logging or analytics before the reducer processes the action.

```python
from hooks import use_reducer


def logging_middleware(state: dict, process: Callable, action: dict) -> dict:
  print("Action: ", action)
  new_state: dict = process(state, action)
  print("New state: ", new_state)
  return new_state


def tasks_reducer(current_state: dict, action: dict) -> dict:
  if action["type"] == "ADD_TASK":
    return {"tasks": current_state["tasks"] + [action["task"]]}
  return current_state


state, dispatch = use_reducer(tasks_reducer, {"tasks": []}, [logging_middleware])

dispatch({"type": "ADD_TASK", "task": "Do the dishes"})
# Output: Action: {"type": "ADD_TASK", "task": "Do the dishes"}
#         New state: {"tasks": ["Do the dishes"]}
```

You may add as many middleware functions as you like. The middleware functions are called in the order they are
provided.

---
### Combining reducers

You may also combine multiple reducers into one using the `combine_reducers` function. This is useful when you want to
split your state into multiple reducers.

```python
from hooks import use_reducer, combine_reducers


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
new_state = dispatch({"type": "SET_USER", "user": "John Doe"})
print(new_state)  # Output: {"tasks": ["Do the dishes"], "user": "John Doe"}
```

The `combine_reducers` function takes in multiple reducer functions and returns a single reducer function. The
returned reducer function will call each reducer function with the current state and action. The returned reducer
function will then combine the results of each reducer function into a single state.

---
### Next steps

Learn about scoping hooks with [hooks_scope](../scoping/scope_decorator.md) decorator.
