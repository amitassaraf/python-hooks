from pyhooks.hooks import use_state
from pyhooks.scope import hook_scope


def test_local_state():
    class Foo:
        @hook_scope(limit_to_keys=["counter_name"])
        def local_state(self, counter_name: str):
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


def test_global_state():
    class Foo:
        @staticmethod
        @hook_scope()
        def global_state(counter_name: str):
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    foo = Foo()

    assert Foo.global_state("A") == 0
    assert foo.global_state("A") == 1
    assert Foo().global_state("A") == 2
    assert Foo().global_state("B") == 0
    assert Foo().global_state("B") == 1


def test_global_state_without_arguments():
    @hook_scope()
    def global_state():
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter

    assert global_state() == 0
    assert global_state() == 1


def test_class_state():
    class Bar:
        @classmethod
        @hook_scope(limit_to_keys=["counter_name"])
        def class_state(cls, counter_name: str):
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    bar = Bar()
    assert Bar.class_state("A") == 0
    assert Bar.class_state("A") == 1
    assert bar.class_state("A") == 2
    assert bar.class_state("B") == 0
    assert bar.class_state("B") == 1


def test_nested_hook_scope():
    class Foo:
        def nested_state(self):
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

        @hook_scope(limit_to_keys=["counter_name"])
        def local_state(self, counter_name: str):
            return self.nested_state()

    foo = Foo()

    assert foo.local_state("A") == 0
    assert foo.local_state("A") == 1
    assert foo.local_state("B") == 0
    assert foo.local_state("B") == 1
    assert foo.local_state("A") == 2
    assert Foo().local_state("A") == 0
    assert Foo().local_state("A") == 0
