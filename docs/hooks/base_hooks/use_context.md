The `use_context` hook allows you to access context from anywhere in your program. This is useful for accessing global state.

Differentiating from the rest of the basic hooks, `use_context` comes along with two other functions `create_context` and `set_context_value`.

`use_context` is used to access the context value. 
`create_context` is used to create a context object. 
`set_context_value` is used to set the context value.

Context, like all hooks, is affected by scoping. This means that context is only accessible within the scope of the function that created (!) it.
Read more about scoping hooks with [hooks_scope](../scoping/hooks_scope.md) decorator.

---
### Creating and using a context

```py
from hooks import create_context, use_context

my_context = create_context("Initial value")

print(use_context(my_context))  # Output: Initial value
```

This is a simple example of creating a context and accessing it with `use_context`. Pretty boring, right? 
Let's make it more interesting.

---
### Setting a context value

```py
from hooks import create_context, use_context, set_context_value

my_context = create_context("Initial value")

print(use_context(my_context))  # Output: Initial value

set_context_value(my_context, "New value")

print(use_context(my_context))  # Output: New value
```

Okay, so now we know how to set a context value. But this is still pretty boring. Let's see how we can use this in a 
real program.

---
### Using context in a real program

```py
from hooks import create_context, use_context, set_context_value

my_context = create_context("Initial value")

def my_stateful_function() -> None:
  print(use_context(my_context))
  return
  
my_stateful_function()  # Output: Initial value

set_context_value(my_context, "New value")

my_stateful_function()  # Output: New value
```

Now this is a bit more interesting. We can see that the context value is updated when we call `set_context_value` and
that the value is accessible from anywhere in the program. 

---
### Why is this useful?

Context is useful for storing global state. This is useful for storing things like the current user, the current theme,
or the current language. 

It is also used as a building block for plugins like `Zustand` and `Redux`.

### Next steps

Learn about [additional hooks](../additional_hooks/use_reducer.md).

Learn about scoping hooks with [hooks_scope](../scoping/hooks_scope.md) decorator. 
