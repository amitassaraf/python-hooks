from hooks import create_context, set_context_value, use_context, use_state

context = create_context("foo")


class Foo:
    def local_state(self):
        foo_or_bar = use_context(context)
        print("foo or bar", foo_or_bar)
        set_context_value(context, "bar")
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        print("local", counter)

    def bad_local_state(not_self):
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        print("bad local", counter)

    @staticmethod
    def good_global_state():
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        print("good global", counter)


class Bar:
    @classmethod
    def class_state(cls):
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        print("class", counter)


def global_state():
    counter, set_counter = use_state(0)
    set_counter(counter + 1)
    print("global", counter)
    foo_or_bar = use_context(context)
    print("foo or bar", foo_or_bar)


if __name__ == "__main__":
    Foo().local_state()
    Foo().local_state()
    foo = Foo()
    foo.local_state()
    foo.local_state()
    foo.bad_local_state()
    foo.bad_local_state()
    foo.good_global_state()
    foo.good_global_state()
    Bar.class_state()
    Bar.class_state()
    global_state()
    global_state()
    global_state()
