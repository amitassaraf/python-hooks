from unittest.mock import Mock

from hooks import use_effect
from hooks.asyncio.use import use_effect as async_use_effect


def test_basic_use() -> None:
    mock = Mock()

    def my_stateful_function() -> None:
        use_effect(lambda: mock(), [])
        return

    my_stateful_function()
    my_stateful_function()
    my_stateful_function()

    assert mock.call_count == 1


def test_use_with_dependencies() -> None:
    mock = Mock()

    def my_stateful_function(name: str) -> None:
        use_effect(lambda: mock(), [name])
        return

    my_stateful_function("John")
    my_stateful_function("John")
    my_stateful_function("Jane")

    assert mock.call_count == 2


def test_use_as_decorator() -> None:
    mock = Mock()

    def my_stateful_function() -> None:
        @use_effect(dependencies=[], decorating=True)
        def my_effect() -> None:
            return mock()

        return

    my_stateful_function()
    my_stateful_function()
    my_stateful_function()

    assert mock.call_count == 1


def test_use_as_decorator_with_dependencies() -> None:
    mock = Mock()

    def my_stateful_function(name: str) -> None:
        @use_effect(dependencies=[name], decorating=True)
        def my_effect() -> None:
            return mock()

        return

    my_stateful_function("John")
    my_stateful_function("John")
    my_stateful_function("Jane")

    assert mock.call_count == 2


async def test_basic_use_async(async_backend) -> None:
    mock = Mock()

    async def my_stateful_function() -> None:
        await async_use_effect(lambda: mock(), [])
        return

    await my_stateful_function()
    await my_stateful_function()
    await my_stateful_function()

    assert mock.call_count == 1


async def test_use_with_dependencies_async(async_backend) -> None:
    mock = Mock()

    async def my_stateful_function(name: str) -> None:
        await async_use_effect(lambda: mock(), [name])
        return

    await my_stateful_function("John")
    await my_stateful_function("John")
    await my_stateful_function("Jane")

    assert mock.call_count == 2
