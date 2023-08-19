from flask import Flask

from hooks import hook_scope, use_state
from hooks.plugins.redis_backend import RedisBackend

app = Flask(__name__)

RedisBackend.use("localhost", 6379)


@app.route("/")
async def get_app_points():
    app_points, set_app_points = await use_state(0)
    set_app_points(app_points + 1)
    return f"App so far got {app_points} points"


@app.route("/user/<username>")
@hook_scope(parametrize=["username"])
def get_user_points(username: str):
    user_points, set_user_points = use_state(0)
    set_user_points(user_points + 1)
    return f"{username} so far got {user_points} points"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9999)
