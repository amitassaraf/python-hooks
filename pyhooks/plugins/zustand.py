from typing import Callable

from box import Box

from pyhooks import create_context, set_context_value, use_context

StateSelector = Callable[[dict], dict]
SetTyping = Callable[[StateSelector], None]
GetTyping = Callable[[None], dict]


class ZustandStore:
    def __init__(self, store_config: Callable[[SetTyping, GetTyping], dict]):
        self.context = create_context({})
        self.setter = lambda state_selector: set_context_value(
            self.context, state_selector
        )
        self.getter = lambda: Box(use_context(self.context))
        set_context_value(self.context, store_config(self.setter, self.getter))

    def __call__(self, selector: StateSelector):
        return selector(self.getter())


def create(store_config: Callable[[SetTyping, GetTyping], dict]) -> ZustandStore:
    """ """
    return ZustandStore(store_config)


use_bear_store = create(
    lambda set, get: (
        {
            "bear": "🐻",
            "set_bear": lambda: set(lambda state: {**state, "bear": "🐻🐻"}),
        }
    )
)


print(use_bear_store(lambda state: state.bear))
