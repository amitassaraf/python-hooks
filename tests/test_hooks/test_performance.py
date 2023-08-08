from cProfile import Profile
from pstats import SortKey, Stats
from statistics import median
from timeit import Timer, timeit

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
    python_state = Timer(Bar().python_state).repeat(repeat=100000, number=1)
    hooks_state = Timer(Foo().local_state).repeat(repeat=100000, number=1)
    python_state = median(python_state)
    hooks_state = median(hooks_state)

    overhead = hooks_state / python_state

    allowed_overhead = 25

    if overhead > allowed_overhead:
        with Profile() as profile:
            timeit(Foo().local_state, number=100000)
            (Stats(profile).strip_dirs().sort_stats(SortKey.TIME).print_stats())
    assert overhead < allowed_overhead, "Performance is not good enough"
