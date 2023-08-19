from hooks.asyncio.use import use_state as async_use_state
from hooks.use import use_state


def test_local_state() -> None:
    class Foo:
        def local_state(self) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    foo = Foo()

    assert foo.local_state() == 0
    assert foo.local_state() == 1
    assert Foo().local_state() == 0
    assert Foo().local_state() == 0


def test_local_state_with_self_renamed() -> None:
    class Foo:
        def local_state(not_self_to_trick_you) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    foo = Foo()

    assert foo.local_state() == 0
    assert foo.local_state() == 1
    assert Foo().local_state() == 0
    assert Foo().local_state() == 0


def test_global_state() -> None:
    class Foo:
        @staticmethod
        def global_state() -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    foo = Foo()

    assert Foo.global_state() == 0
    assert foo.global_state() == 1
    assert Foo().global_state() == 2

    def global_state() -> int:
        counter, set_counter = use_state(0)
        set_counter(counter + 1)
        return counter

    assert global_state() == 0
    assert global_state() == 1


def test_class_state() -> None:
    class Bar:
        @classmethod
        def class_state(cls) -> int:
            counter, set_counter = use_state(0)
            set_counter(counter + 1)
            return counter

    bar = Bar()
    assert Bar.class_state() == 0
    assert Bar.class_state() == 1
    assert bar.class_state() == 2


async def test_local_state_async(async_backend) -> None:
    class Foo:
        async def local_state(self) -> int:
            counter, set_counter = await async_use_state(0)
            await set_counter(counter + 1)
            return counter

    foo = Foo()

    assert await foo.local_state() == 0
    assert await foo.local_state() == 1
    assert await Foo().local_state() == 0
    assert await Foo().local_state() == 0


async def test_local_two_state_async(async_backend) -> None:
    class Foo:
        async def local_state(self) -> tuple[int, int]:
            counter, set_counter = await async_use_state(0)
            await set_counter(counter + 1)
            other_counter, set_other_counter = await async_use_state(0)
            return counter, other_counter

    foo = Foo()

    assert await foo.local_state() == (0, 0)
    assert await foo.local_state() == (1, 0)
    assert await Foo().local_state() == (0, 0)
    assert await Foo().local_state() == (0, 0)


async def test_local_state_with_self_renamed_async(async_backend) -> None:
    class Foo:
        async def local_state(not_self_to_trick_you) -> int:
            counter, set_counter = await async_use_state(0)
            await set_counter(counter + 1)
            return counter

    foo = Foo()

    assert await foo.local_state() == 0
    assert await foo.local_state() == 1
    assert await Foo().local_state() == 0
    assert await Foo().local_state() == 0


async def test_global_state_async(async_backend) -> None:
    class Foo:
        @staticmethod
        async def global_state() -> int:
            counter, set_counter = await async_use_state(0)
            await set_counter(counter + 1)
            return counter

    foo = Foo()

    assert await Foo.global_state() == 0
    assert await foo.global_state() == 1
    assert await Foo().global_state() == 2

    async def global_state() -> int:
        counter, set_counter = await async_use_state(0)
        await set_counter(counter + 1)
        return counter

    assert await global_state() == 0
    assert await global_state() == 1


async def test_class_state_async(async_backend) -> None:
    class Bar:
        @classmethod
        async def class_state(cls) -> int:
            counter, set_counter = await async_use_state(0)
            await set_counter(counter + 1)
            return counter

    bar = Bar()
    assert await Bar.class_state() == 0
    assert await Bar.class_state() == 1
    assert await bar.class_state() == 2
