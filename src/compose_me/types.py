from typing import Any, Protocol


class _FilterArg(Protocol):
    """
    Signature of the function decorated with #filter().
    """

    __name__: str

    def __call__(self, _value: Any) -> Any:
        ...


class _FilterDecorator(Protocol):
    """
    Type of the wrapper function returned by #filter().
    """

    def __call__(self, _func: _FilterArg) -> _FilterArg:
        ...


class _FilterFunction(Protocol):
    """
    Type of the #filter() decorator function.
    """

    def __call__(self) -> _FilterDecorator:
        ...
