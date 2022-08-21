from typing import Any, Callable, Coroutine, TypeVar

CORO = Callable[..., Coroutine[Any, Any, Any]]

Sanic = TypeVar("Sanic")
