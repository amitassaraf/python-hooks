from typing import Any, Union


class __Destruct:
    def __init__(self, wrapped_object: Any) -> None:
        self.wrapped_object = wrapped_object

    def __getitem__(self, items: Any) -> Union[Any, tuple, None]:
        if not isinstance(items, (list, tuple)):
            items = [items]

        output = []
        for item in items:
            try:
                output.append(self.wrapped_object[item])
            except (
                IndexError,
                KeyError,
                TypeError,
            ):
                if isinstance(self.wrapped_object, (dict,)):
                    output.append(self.wrapped_object.get(item))
                elif hasattr(self.wrapped_object, str(item)):
                    output.append(getattr(self.wrapped_object, str(item)))
        if len(output) == 1:
            return output[0]
        elif len(output) == 0:
            return None
        return tuple(output)


def destruct(wrapped_object: Any) -> __Destruct:
    """
    A utility function to allow destructuring of objects in a similar way to JavaScript. For example:
    const {name} = useData({name: "John", count: 0})

    This is equivalent to:
    name = destruct(useData({name: "John", count: 0}))["name"]

    :param wrapped_object: The object to destructure
    :return: A __Destruct object that can be used to destructure the wrapped object
    """
    return __Destruct(wrapped_object)


# Alias for destruct
d = destruct
