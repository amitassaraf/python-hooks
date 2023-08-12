The Zustand plugin is a state management plugin that is inspired by the [Zustand](https://github.com/pmndrs/zustand) library.

It is basically a wrapper around `use_context` to provide a more familiar API for Zustand users.

### Installation

```bash
pip install python-hooks[zustand]
```

### Usage

```python
from hooks.plugins.zustand import create

use_bear_store = create(
    {
        "bear": "🐻",
    },
    lambda set, get: (
        {
            "increase_bears": lambda: set(lambda state: {**state, "bear": "🐻🐻"}),
        }
    ),
)


def test_basic_get_and_set() -> None:
    print(use_bear_store(lambda state: state.bear))  # Output: "🐻"

    increase_bears = use_bear_store(lambda state: state.increase_bears)
    increase_bears()

    print(use_bear_store(lambda state: state.bear))  # Output: "🐻🐻"
```
