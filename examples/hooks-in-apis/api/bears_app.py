from flask import Flask

from hooks.backend import set_hooks_backend
from hooks.plugins.redis_backend import RedisHooksBackend
from hooks.plugins.zustand import create

app = Flask(__name__)

RedisHooksBackend.initialize("localhost", 6379)
set_hooks_backend(RedisHooksBackend)

use_bear_store = create(
    {
        "bears": "🐻",
    },
    lambda set, get: (
        {
            "increase_bears": lambda: set(
                lambda state: {**state, "bears": state["bears"] + "🐻"}
            ),
        }
    ),
)

increase_bears = use_bear_store(lambda state: state.increase_bears)


@app.route("/")
def get_bears():
    increase_bears()
    return use_bear_store(lambda state: state.bears)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9999)