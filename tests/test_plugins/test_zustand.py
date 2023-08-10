from hooks.plugins.zustand import create

use_bear_store = create(
    lambda set, get: (
        {
            "bear": "🐻",
            "increase_bears": lambda: set(lambda state: {**state, "bear": "🐻🐻"}),
        }
    )
)


def test_basic_get_and_set() -> None:
    assert use_bear_store(lambda state: state.bear) == "🐻"

    increase_bears = use_bear_store(lambda state: state.increase_bears)
    increase_bears()

    assert use_bear_store(lambda state: state.bear) == "🐻🐻"
