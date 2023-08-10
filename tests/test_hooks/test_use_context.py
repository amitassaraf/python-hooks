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
