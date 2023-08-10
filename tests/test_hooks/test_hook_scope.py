from hooks.scope import hook_scope
from hooks.use import use_state


def test_local_state() -> None:
    class Foo:
        @hook_scope(limit_to_keys=["counter_name"])
        def local_state(self, counter_name: str) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    foo = Foo()

    assert foo.local_state("A") == 0
    assert foo.local_state("A") == 1
    assert foo.local_state("B") == 0
    assert foo.local_state("B") == 1
    assert foo.local_state("A") == 2
    assert Foo().local_state("A") == 0
    assert Foo().local_state("A") == 0


def test_global_state() -> None:
    class Foo:
        @staticmethod
        @hook_scope()
        def global_state(counter_name: str) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    foo = Foo()

    assert Foo.global_state("A") == 0
    assert foo.global_state("A") == 1
    assert Foo().global_state("A") == 2
    assert Foo().global_state("B") == 0
    assert Foo().global_state("B") == 1


def test_global_state_without_arguments() -> None:
    @hook_scope()
    def global_state() -> int:
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter

    assert global_state() == 0
    assert global_state() == 1


def test_class_state() -> None:
    class Bar:
        @classmethod
        @hook_scope(limit_to_keys=["counter_name"])
        def class_state(cls, counter_name: str) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    bar = Bar()
    assert Bar.class_state("A") == 0
    assert Bar.class_state("A") == 1
    assert bar.class_state("A") == 2
    assert bar.class_state("B") == 0
    assert bar.class_state("B") == 1


def test_hook_scope_of_nested_functions() -> None:
    class Foo:
        def nested_state(self) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

        @hook_scope(limit_to_keys=["counter_name"])
        def local_state(self, counter_name: str) -> int:
            return self.nested_state()

    foo = Foo()

    assert foo.local_state("A") == 0
    assert foo.local_state("A") == 1
    assert foo.local_state("B") == 0
    assert foo.local_state("B") == 1
    assert foo.local_state("A") == 2
    assert Foo().local_state("A") == 0
    assert Foo().local_state("A") == 0


def test_nested_hook_scopes() -> None:
    class Foo:
        @hook_scope()
        def nested_state_with_scope(self) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

        @hook_scope(limit_to_keys=["counter_name"])
        def local_state(self, counter_name: str) -> int:
            return self.nested_state_with_scope()

    foo = Foo()

    assert foo.local_state("A") == 0
    assert foo.local_state("A") == 1
    assert foo.local_state("B") == 0
    assert foo.local_state("B") == 1
    assert foo.local_state("A") == 2
    assert Foo().local_state("A") == 0
    assert Foo().local_state("A") == 0


def test_local_state_that_is_scoped_globally() -> None:
    class Foo:
        @hook_scope(use_global_scope=True, limit_to_keys=[])
        def local_state(self) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    foo = Foo()

    assert foo.local_state() == 0
    assert foo.local_state() == 1
    assert Foo().local_state() == 2
    assert Foo().local_state() == 3
