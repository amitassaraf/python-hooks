# mypy: ignore-errors

from typing import Any, Callable

from box import Box

from hooks import create_context, set_context_value, use_context

StateSelector = Callable[[Any], Any]
SetTyping = Callable[[StateSelector], None]
GetTyping = Callable[[], Box]


class ZustandStore:
    def __init__(
        self,
        store_initial_state: dict[str, Any],
        store_config: Callable[[SetTyping, GetTyping], Any],
    ):
        self.state_context = create_context(store_initial_state)
        self.config_context = create_context({})

        def setter(state_selector: StateSelector) -> None:
            set_context_value(
                self.state_context,
                state_selector(use_context(self.state_context)),
            )

        def getter() -> Box:
            return Box(
                {**use_context(self.state_context), **use_context(self.config_context)}
            )

        self.setter = setter
        self.getter = getter
        set_context_value(
            self.config_context,
            store_config(self.setter, self.getter),
        )

    def __call__(self, selector: StateSelector) -> Any:
        return selector(self.getter())


def create(
    store_initial_state: dict[str, Any],
    store_config: Callable[[SetTyping, GetTyping], Any],
) -> ZustandStore:
    """ """
    return ZustandStore(store_initial_state, store_config)
