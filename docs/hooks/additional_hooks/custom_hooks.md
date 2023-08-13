Sometimes it would make sense to write custom hooks. For example, you may want to create a custom hook to fetch data 
from a database or to fetch data from a file. Or you might want to write a custom hook that combines functionality from
multiple hooks. 

To do this, it's very simple. Just write a function that it's name starts with `use_` and it will be treated as a hook.
For example, let's say we want to write a custom hook that combines the functionality of `use_state` and `use_effect`:

```python
from hooks import use_state, use_effect
from hooks.utils import destruct


def use_state_and_effect(initial_state: int):
  state, set_state = use_state(initial_state)

  def effect():
    print("State changed: ", state)

  use_effect(effect, [state])

  # Returning in a dict just as an example for using destruct (The util will work on any object)
  return {
    "state": state,
    "set_state": set_state
  }
  

set_state = destruct(use_state_and_effect(0))["set_state"]
set_state(1)
set_state(2)
set_state(3)
```

__Note__: You have to use the `use_` prefix in order for the hook to be treated as a hook. Otherwise, it will be treated
as a normal function and will not be able to identify where to store the state inside the backend.

---
### Next steps

Learn about scoping hooks with [hooks_scope](../scoping/scope_decorator.md) decorator.
