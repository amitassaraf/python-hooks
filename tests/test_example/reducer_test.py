from reducers import use_reducer


def tasks_reducer(current_state, action):
    if action["type"] == "ADD_TASK":
        return {"tasks": current_state["tasks"] + [action["task"]]}
    return current_state


def logging_middleware(state, next, action):
    print("Previous state:", state)
    new_state = next(state, action)
    print("New state:", new_state)
    return new_state


def main():
    state, dispatch = use_reducer(tasks_reducer, {"tasks": []}, [logging_middleware])

    dispatch({"type": "ADD_TASK", "task": "Do the dishes"})


if __name__ == "__main__":
    main()
    main()
