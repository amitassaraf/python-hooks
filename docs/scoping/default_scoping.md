By default, hooks are scoped to the smallest enclosing scope. This means that if you call a hook inside a function, the
hook will only be scoped to that function. If you call a hook inside a class, the hook will only be scoped to that
class. If you call a hook inside a module, the hook will only be scoped to that module.

Hooks scoping mechanism attempts to work in a very predictable way in order to avoid unexpected behavior. 

Here is an example of how hooks are scoped to the smallest enclosing scope:

```python
from hooks import use_state


def get_tasks():
  state, set_state = use_state({"tasks": []})
  return state["tasks"]


print(get_tasks())  # Output: []


def add_task(task: str):
  state, set_state = use_state()
  set_state({"tasks": state["tasks"] + [task]})


add_task("Do the dishes")
add_task("Do the laundry")
print(get_tasks())  # Output: []
```

As you can see in the example above, the `get_tasks` function is scoped to the `get_tasks` function, and the `add_task`
function is scoped to the `add_task` function. This means that the `get_tasks` function will always return an empty
list,
and the `add_task` function will always add a task to an empty list.

---
### Class scopes

When using hooks inside a class, the scope by default will be limited to that class according to the type of method
that the hook is called in. For example, if you call a hook inside a `classmethod`, the hook will be scoped to the class
and not the instance. If you call a hook inside an `instancemethod`, the hook will be scoped to the instance and not the
class. If you call a hook inside a `staticmethod`, the hook will be scoped globally.

```python
from hooks import use_state


class CounterClass:
    def instance_counter(self):
        count, set_count = use_state(0)
        set_count(count + 1)
        return count

    @classmethod
    def class_counter(cls):
        count, set_count = use_state(0)
        set_count(count + 1)
        return count

    @staticmethod
    def static_counter():
        count, set_count = use_state(0)
        set_count(count + 1)
        return count


counter = CounterClass()
print(counter.instance_counter())         # Output: 0
print(counter.instance_counter())         # Output: 1
print(CounterClass().instance_counter())  # Output: 0
print(CounterClass().instance_counter())  # Output: 0
print(CounterClass.class_counter())       # Output: 0
print(CounterClass.class_counter())       # Output: 1
print(CounterClass.static_counter())      # Output: 0
```

As you can see the default scoping mechanism for hooks inside a class is to scope the hook to the smallest enclosing
scope and is predictable. However, you may want to change the default scoping mechanism for hooks inside a class. You
can do this by using the [hooks_scope](scope_decorator.md) decorator.

---

### Scopes and function parameters

When using hooks inside a function, the scope by default will ignore function parameters. This means that if you call a
hook inside a function, the hook will be scoped to the function and not the function parameters (Unless when using 
parameters as dependencies on [use_effect](../hooks/base_hooks/use_effect.md)).

```python
from hooks import use_state


def get_count(other_param: str):
    count, set_count = use_state(0)
    set_count(count + 1)
    print(other_param)
    return count
    

print(get_count("Hello"))  # Output: 0
print(get_count("World"))  # Output: 1
print(get_count("This wont affect the state"))  # Output: 2
```  

---
### Next steps

Learn about scoping hooks with [hooks_scope](../scoping/scope_decorator.md) decorator.
