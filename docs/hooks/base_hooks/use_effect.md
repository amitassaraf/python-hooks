The `use_effect` hook allows us to run code when the state of the program changes. This is useful for running code when
the program starts, or when the user interacts with the program, or it's dependencies change.

---

### Basic use

```py
use_effect(lambda: print("Hello World"), [])
```

The `use_effect` hook takes two arguments. The first argument is a function which will be called when the state of the
program changes.
The second argument is a list of dependencies. The function will only be called when the dependencies change and at
least once when the program starts.

Let's see an example:

```py
from hooks import use_effect


def my_stateful_function() -> None:
  # Will only print "Hello World" once, during the first function call
  use_effect(lambda: print("Hello World"), [])
  return


my_stateful_function()  # Output: Hello World
my_stateful_function()  # Output: 
my_stateful_function()  # Output: 
```

---

### Dependencies

The second argument to `use_effect` is a list of dependencies. The function will only be called when the dependencies
change and at least once when the program starts.

```py
from hooks import use_effect


def my_stateful_function(name: str) -> None:
  # Will only print "Hello, {name}" when the name changes
  use_effect(lambda: print(f"Hello, {name}"), [name])
  return


my_stateful_function("John")  # Output: Hello, John
my_stateful_function("John")  # Output:
my_stateful_function("Jane")  # Output: Hello, Jane
my_stateful_function("Jane")  # Output:
```

As you can see in the example above, the function is only called when the name changes. This is akin to caching the
result of the function using something like functool's `lrucache`.
The main difference is that you may cache different actions inside the function instead of the entire function itself which is pretty neat.

---
### As a decorator

The `use_effect` hook can also be used as a decorator. This is useful when your use_effect hook is longer than a single line.

```py
from hooks import use_effect

def my_stateful_function(name: str) -> None:
  
  @use_effect(dependencies=[name], decorating=True)
  def my_effect():
    print(f"Hello, {name}")
  
  return
  
my_stateful_function("John")  # Output: Hello, John
my_stateful_function("John")  # Output:
my_stateful_function("Jane")  # Output: Hello, Jane
my_stateful_function("Jane")  # Output:
```

### Next steps

Learn the next basic hook: [use_context](use_context.md)
