The `use_state` hook is the most basic hook in the library. It allows you to store state in a function. It's similar to the `useState` hook in React.
All other hooks are built on top of this hook.

---

### Basic use

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
State may be persisted for longer periods of time by using a different [backend](../../backends/default.md).
---
### Multiple state hooks

Additionally, we can use multiple `use_state` hooks in a single function. This allows us to store multiple pieces of state in a single function.

```py
from hooks import use_state

def my_stateful_function() -> tuple[int, str]:
    count, set_count = use_state(0)
    name, set_name = use_state("John")
    set_count(count + 1)
    set_name("Jane")
    return count, name

print(my_stateful_function()) # Output: (0, "John")
print(my_stateful_function()) # Output: (1, "Jane")
print(my_stateful_function()) # Output: (2, "Jane")
```

---

### State hooks inside objects

We can also use `use_state` hooks inside objects. This allows us to store state which is persisted for the lifetime of the object.

```py
from hooks import use_state

class MyObject:
    def object_persisted_count(self):
        count, set_count = use_state(0)
        set_count(count + 1)
        return count

obj = MyObject()
print(obj.object_persisted_count())          # Output: 0
print(obj.object_persisted_count())          # Output: 1

my_other_obj = MyObject()
print(my_other_obj.object_persisted_count()) # Output: 0
```

---
### Class methods and static methods

The `use_state` hook can also be used inside class methods and static methods. This allows us to store state which is persisted for the lifetime of the class.

```py
from hooks import use_state

class MyClass:
    @classmethod
    def class_persisted_count(cls):
        count, set_count = use_state(0)
        set_count(count + 1)
        return count

    @staticmethod
    def static_persisted_count():
        count, set_count = use_state(0)
        set_count(count + 1)
        return count

print(MyClass.class_persisted_count())  # Output: 0
print(MyClass.class_persisted_count())  # Output: 1

print(MyClass.static_persisted_count()) # Output: 0
print(MyClass.static_persisted_count()) # Output: 1
```

__Note:__ the inner workings of hooks are not dependent on the naming of the arguments, meaning you do not have to name
the instance or class arguments `self` and `cls` for the hooks to work.
You can name them whatever you want.
---
### Thread safety of state hooks

<img src="https://img.shields.io/badge/⚠️ use_state is currently not threadsafe by default-ff9966" />

The `use_state` hook is currently not threadsafe. The reason being that the default backend is not threadsafe in order
to maximize compatibility with different frameworks such as Flask. If you need to use `use_state` in a 
multithreaded environment you should use the `threadsafe` backend. See [Backends](../../backends/default.md) for more information.

---
### Next steps

Learn the next basic hook: [use_effect](use_effect.md)
