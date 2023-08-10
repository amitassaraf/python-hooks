from typing import Any, Callable

from box import Box

from hooks import create_context, set_context_value, use_context

StateSelector = Callable[[Any], Any]
SetTyping = Callable[[StateSelector], None]
GetTyping = Callable[[], Box]


class ZustandStore:
    def __init__(self, store_config: Callable[[SetTyping, GetTyping], Any]):
        self.context = create_context({})
        self.setter = lambda state_selector: set_context_value(
            self.context, state_selector(use_context(self.context))
        )
        self.getter = lambda: Box(use_context(self.context))
        set_context_value(self.context, store_config(self.setter, self.getter))

    def __call__(self, selector: StateSelector) -> Any:
        return selector(self.getter())


def create(store_config: Callable[[SetTyping, GetTyping], Any]) -> ZustandStore:
    """ """
    return ZustandStore(store_config)
