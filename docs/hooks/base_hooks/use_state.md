The `use_state` hook is the most basic hook in the library. It allows you to store state in a function. It's similar to the `useState` hook in React.
All other hooks are built on top of this hook.

Let learn about `use_state`:
```py
count, set_count = use_state(0)
```

`use_state` will always return a tuple of the current state and a function to update the state. The state can be any type, it can be a string, a number, a list or a dictionary.

The state will automatically be persisted between function calls. See [Default Scoping](../../scoping/default.md) for more information on how the state is persisted.

Let's see an example:

```py
# We import the use_state hook from the hooks module
from hooks import use_state

def my_stateful_function() -> int:
    # We call the use_state hook and store the result in a variable called count and set_count
    count, set_count = use_state(0)
    # We mutate the state by adding 1 to the current count
    set_count(count + 1) 
    return count

print(my_stateful_function()) # Output: 0
print(my_stateful_function()) # Output: 1
print(my_stateful_function()) # Output: 2
```

As you can see, the state is persisted between function calls. This is because the state is stored in the function's scope.
By default, the state is persisted only for the duration of the program. If you run the program again, the state will be reset.
State may be persisted for longer periods of time by using a different [backend](../../backends/README.md).

<img src="https://img.shields.io/badge/⚠️ use_state is currently not threadsafe by default-ff9966" />

The `use_state` hook is currently not threadsafe. The reason being that the default backend is not threadsafe in order
to maximize compatibility with different frameworks such as Flask. If you need to use `use_state` in a 
multithreaded environment you should use the `threadsafe` backend. See [Backends](../../backends/README.md) for more information.
