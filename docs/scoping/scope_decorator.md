The `@hook_scope` decorator is used to define a scope for your hooks. It is useful for two main use cases:

* When you want to persist state based on function parameters.
* When you want to scope hooks in a method globally instead of to the instance or class.

---
### Scoping state to function parameters

When using hooks inside a function, the scope by default will ignore function parameters. This means that if you call a
hook inside a function, the hook will be scoped to the function and not the function parameters (Unless when using
parameters as dependencies on [use_effect](../hooks/base_hooks/use_effect.md)).

You can use the `@hook_scope` decorator to scope hooks to function parameters. This is useful when you want to persist
state based on function parameters.

```python
from hooks import use_state, hook_scope


@hook_scope(limit_to_keys=["owner"])
def owned_counter(owner: str):
    count, set_count = use_state(0)
    set_count(count + 1)
    print(f"{owner}'s count is {count}")

owned_counter("John")  # Output: John's count is 0
owned_counter("John")  # Output: John's count is 1
owned_counter("Jane")  # Output: Jane's count is 0
owned_counter("Jane")  # Output: Jane's count is 1
```

Note that you do not have to provide a value for the `limit_to_keys` parameter. If you do not provide a value, the hook
will be scoped to all function parameters.

```python
from hooks import use_state, hook_scope


@hook_scope()
def owned_counter(owner: str):
    count, set_count = use_state(0)
    set_count(count + 1)
    print(f"{owner}'s count is {count}")

owned_counter("John")  # Output: John's count is 0
owned_counter("John")  # Output: John's count is 1
owned_counter("Jane")  # Output: Jane's count is 0
owned_counter("Jane")  # Output: Jane's count is 1
```

---
### Scoping hooks globally

When using hooks inside a class, the default scoping mechanism is to scope the hook to the smallest enclosing scope.
Sometimes, you'll want to scope hooks globally instead of to the instance or class. You can do this by using the
`@hook_scope` decorator.

```python
from hooks import use_state, hook_scope


class CounterClass:
    @hook_scope(use_global_scope=True, limit_to_keys=[])
    def instance_method_scoped_globally(self):
        count, set_count = use_state(0)
        set_count(count + 1)
        return count
        
    def instance_method(self):
        count, set_count = use_state(0)
        set_count(count + 1)
        return count


counter = CounterClass()
counter_two = CounterClass()
print(counter.instance_method())                      # Output: 0
print(counter.instance_method())                      # Output: 1
print(counter_two.instance_method())                  # Output: 0
print(counter.instance_method_scoped_globally())      # Output: 0
print(counter_two.instance_method_scoped_globally())  # Output: 1

```

Note that when using `use_global_scope=True`, you have to provide a value for the `limit_to_keys` parameter. You may
provide an empty list if you want to scope the hook to no parameters.


---
### Nesting scopes

As you might be aware hooks can be used anywhere and you may have functions that use hooks and are called by other
functions that use hooks. When nesting hooks like this, scoping will affect all hooks in the call stack.

```python 
from hooks import use_state, hook_scope

class NestedStates:
    def nested_state(self) -> int:
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter

    @hook_scope(limit_to_keys=["counter_name"])
    def local_state(self, counter_name: str) -> int:
        return self.nested_state()

foo = NestedStates()
    
print(foo.local_state("A"))            # Output: 0
print(foo.local_state("A"))            # Output: 1

# As you can see the scope of local_state affects the nested_state's function hooks.
print(foo.local_state("B"))            # Output: 0
print(foo.local_state("B"))            # Output: 1
print(foo.local_state("A"))            # Output: 2

print(NestedStates().local_state("A")) # Output: 0
print(NestedStates().local_state("A")) # Output: 0

```

The same concept can be taken further by scoping the nested_state function.

```python
from hooks import use_state, hook_scope

class NestedStates:
    @hook_scope()
    def nested_state_with_scope(self) -> int:
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter
  
    @hook_scope(limit_to_keys=["counter_name"])
    def local_state(self, counter_name: str) -> int:
        return self.nested_state_with_scope()

foo = NestedStates()

print(foo.local_state("A"))             # Output: 0
print(foo.local_state("A"))             # Output: 1

print(foo.local_state("B"))             # Output: 0
print(foo.local_state("B"))             # Output: 1
print(foo.local_state("A"))             # Output: 2

print(NestedStates().local_state("A"))  # Output: 0
print(NestedStates().local_state("A"))  # Output: 0
```

---

### Next steps

Learn about [backends](../backends/scope_decorator.md).
