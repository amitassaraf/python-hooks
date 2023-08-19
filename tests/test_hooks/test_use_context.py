from hooks.asyncio.use import create_context as create_async_context
from hooks.asyncio.use import set_context_value as async_set_context_value
from hooks.asyncio.use import use_context as async_use_context
from hooks.use import create_context, set_context_value, use_context


def test_context_hook() -> None:
    context = create_context("foo")

    def flip_according_to_context_value() -> str:
        foo_or_bar = use_context(context)
        if foo_or_bar == "foo":
            return "bar"
        return "foo"

    assert flip_according_to_context_value() == "bar"
    set_context_value(context, "bar")
    assert flip_according_to_context_value() == "foo"


async def test_context_hook_async(async_backend) -> None:
    context = await create_async_context("foo")

    async def flip_according_to_context_value() -> str:
        foo_or_bar = await async_use_context(context)
        if foo_or_bar == "foo":
            return "bar"
        return "foo"

    assert await flip_according_to_context_value() == "bar"
    await async_set_context_value(context, "bar")
    assert await flip_according_to_context_value() == "foo"
