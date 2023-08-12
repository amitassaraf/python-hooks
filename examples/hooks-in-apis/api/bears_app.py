from flask import Flask

from hooks.plugins.redis_backend import RedisBackend
from hooks.plugins.zustand import create

app = Flask(__name__)

RedisBackend.use("localhost", 6379)

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
