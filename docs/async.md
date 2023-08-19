Lately, support in async / await has been added to Python Hooks. This allows you to write asynchronous code in your hooks. 
This is especially useful for hooks that need to make network requests or perform other I/O operations.

To use async / await hooks, all you need to do is import your hooks from `hooks.asyncio.*` instead of `hooks.*`,
and make sure that you are using an async backend, such as `hooks.plugins.redis_backend.AsyncRedisBackend`.

For example:

```python
from hooks.asyncio.use import use_state
from hooks.plugins.redis_backend import AsyncRedisBackend

... 

await AsyncRedisBackend.use('localhost', 6789)

async def use_async_state():
    state, set_state = await use_state(0)
    await set_state(state + 1)
    return state

...

print(await use_async_state()) # prints 0
print(await use_async_state()) # prints 1
```
