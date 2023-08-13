from hooks import use_state


def test_custom_counter_hook() -> None:
    def use_counter() -> int:
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter

    class Foo:
        def local_state(self) -> int:
            return use_counter()

        def other_local_state(self) -> int:
            return use_counter()

    foo = Foo()

    assert foo.local_state() == 0
    assert foo.local_state() == 1
    assert foo.other_local_state() == 0
    assert foo.other_local_state() == 1
    assert Foo().local_state() == 0
    assert Foo().local_state() == 0
    assert Foo().other_local_state() == 0


def test_custom_counter_hook_when_not_using_use_prefix() -> None:
    def wrongly_named_counter() -> int:
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter

    class Foo:
        def local_state(self) -> int:
            return wrongly_named_counter()

        def other_local_state(self) -> int:
            return wrongly_named_counter()

    foo = Foo()

    assert foo.local_state() == 0
    assert foo.local_state() == 1
    assert foo.other_local_state() == 2
    assert foo.other_local_state() == 3
    assert Foo().local_state() == 4
    assert Foo().local_state() == 5
    assert Foo().other_local_state() == 6
