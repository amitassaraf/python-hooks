from pyhooks.plugins.zustand import create

use_bear_store = create(
    lambda set, get: (
        {
            "bear": "🐻",
            "set_bear": lambda: set(lambda state: {**state, "bear": "🐻🐻"}),
        }
    )
)


def test_basic_get_and_set():
    assert use_bear_store(lambda state: state.bear) == "🐻"

    use_bear_store(lambda state: state.set_bear)()

    assert use_bear_store(lambda state: state.bear) == "🐻🐻"
