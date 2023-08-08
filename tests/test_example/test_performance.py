from timeit import timeit

from pyhooks.hooks import use_state


class Foo:
    def local_state(self):
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter


class Bar:
    def __init__(self):
        self.counter = 0

    def python_state(self):
        self.counter += 1
        return self.counter


def test_local_state():
    python_state = timeit(Bar().python_state, number=100000)
    hooks_state = timeit(Foo().local_state, number=100000)
    assert hooks_state < python_state * 50, "Performance is not good enough"
