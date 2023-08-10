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
        self.context = create_context({"state": store_initial_state})

        def setter(state_selector: StateSelector) -> None:
            inner_state = self.getter()
            set_context_value(
                self.context,
                {
                    "state": state_selector(inner_state.state.to_dict()),
                    "config": inner_state.config,
                },
            )

        def getter() -> Box:
            return Box(use_context(self.context))

        self.setter = setter
        self.getter = getter
        set_context_value(
            self.context,
            {**self.getter(), "config": store_config(self.setter, self.getter)},
        )

    def __call__(self, selector: StateSelector) -> Any:
        inner_state = self.getter()
        return selector(
            Box({**inner_state.state.to_dict(), **inner_state.config.to_dict()})
        )


def create(
    store_initial_state: dict[str, Any],
    store_config: Callable[[SetTyping, GetTyping], Any],
) -> ZustandStore:
    """ """
    return ZustandStore(store_initial_state, store_config)
