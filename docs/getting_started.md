# 🚀 Getting Started

In order to get started with Python Hooks, you need to install the library using pip, note that when installing 
the library you install it as `python-hooks` and not `hooks` as the latter is already taken in pip. 

```bash
pip install python-hooks
```

Once installed you can start using the library, the library is built with plugins support and you can use the built-in plugins or create your own.

```py 
from hooks import use_state, use_effect

def my_stateful_function():
    count, set_count = use_state(0)
    use_effect(lambda: print("First run"), [])
    use_effect(lambda: print(f"Count, {count}"), [count]) # (1)
    set_count(count + 1) 
    return count

my_stateful_function() # prints "First run" and "Count, 0"
my_stateful_function() # prints "Count, 1"
my_stateful_function() # prints "Count, 2"
```

1.  🤩 Just like React, use_effect will only run if it's dependencies have changed. In this case, the dependency is the count variable. 
    This is a very powerful feature as it allows you to control when your code runs.


See [Hooks](hooks/base_hooks/use_state.md) to begin using the built-in hooks.
