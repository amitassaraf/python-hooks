Under the hood, Python Hooks uses backend objects to store the state of hooks. This provides a way to persist state
in different ways by using different backends. By default, Python Hooks uses the `MemoryBackend` to store state in
memory, but you can also use the `RedisBackend` to store state in Redis, or you can create your own custom backend
to store state in any way you want.

#### Backends available out of the box:
* MemoryBackend - Pickled state stored in memory
* RedisBackend - Pickled state stored in Redis
* ThreadsafeBackend - Pickled state stored in a thread local data structure

---

### Changing the default backend

Changing the in-use backend is super easy. 

```python
from hooks.backends import ThreadsafeBackend

ThreadsafeBackend.use()

# Any hooks created after this point will use the ThreadsafeBackend
```

or for using Redis:

```python
from hooks.backends import RedisBackend

RedisBackend.use("localhost", 6379, db=0)

# Any hooks created after this point will use the RedisBackend
```

---

### Creating a custom backend

You can create a custom backend by just inheriting from the `HooksBackend` class and implementing subset of the methods
defined in the `HooksBackend` class. 
