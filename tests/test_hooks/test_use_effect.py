from unittest.mock import Mock

from hooks import use_effect


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
