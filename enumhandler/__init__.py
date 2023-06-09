from enum import Enum, auto
from inspect import getmembers
from typing import Callable, Generic, Self, Type, TypeVar

E = TypeVar("E", bound=Type[Enum])
M = TypeVar("M", bound=Enum)
O = TypeVar("O")  # noqa: E741


class CacheStrategy(Enum):
    NO_CACHE = auto()
    EAGER_CACHE = auto()
    LAZY_CACHE = auto()

    def use_cache(self):
        return self is not CacheStrategy.NO_CACHE


class EnumHandler(Generic[E, M, O]):
    """
    A callable handler for the members of an enum. Implementations should subclass this
    class, and then use the ``EnumHandler.register`` decorator (also exported as
    ``handles``) to register one handler per member of the enum.

    For example, consider an enumeration of mathematical operations::

        class Operations(Enum):
            ADD = auto()
            MUL = auto()
            AVG = auto()

    Along with an implementation of a handler for them::

        class OperationHandler(EnumHandler, enum=Operations):
            EnumHandler.register(Operations.ADD)
            def add(self, *args):
                return sum(args)

            EnumHandler.register(Operations.MUL)
            def multiply(self, *args):
                return reduce(lambda acc, n: acc * n)

            EnumHandler.register(Operations.AVG)
            def average(self, *args):
                return sum(args) / len(args)

    The user will then instantiate the subclass using an enum member, and can treat it
    as a callable::

        adder = OperationHandler(Operations.ADD)
        adder(3, 4, 5)
    """

    _final: bool = False
    _handlers: dict[E, Callable[..., O]]
    _handler: Callable[..., O]

    _cache_strategy: CacheStrategy
    _instance_cache: dict[E, Self]

    def __new__(cls, enum_element):
        if cls._cache_strategy.use_cache():
            try:
                return cls._instance_cache[enum_element]
            except KeyError:
                instance = super().__new__(cls)
                instance.__init__(enum_element)
                cls._instance_cache[enum_element] = instance
                return instance

        return super().__new__(cls)

    def __init__(self, enum_element):
        self._handler = self._handlers[enum_element]

        if handler_doc := self._handler.__doc__:
            self.__doc__ = handler_doc

    def __call__(self, *args, **kwargs) -> O:
        try:
            return self._handler(self, *args, **kwargs)
        except AttributeError as ex:
            raise NotImplementedError(
                "EnumHandler must be subclassed and instantiated."
            ) from ex

    def __init_subclass__(
        cls, *, enum: E, cache: CacheStrategy = CacheStrategy.EAGER_CACHE
    ):
        """
        Registers handlers for each member of the given enum class, typechecks the
        registered handlers, and raises errors for duplicates, non-exhaustive handlers,
        or members of unexpected enum classes.
        """
        cls._cache_strategy = cache
        cls._final = True
        cls._handlers = {}
        cls._instance_cache = {}

        for method in (attr for _, attr in getmembers(cls) if callable(attr)):
            try:
                for enum_value in method._handles:
                    if enum_value in cls._handlers:
                        raise InvalidEnumHandler(
                            f"Multiple handlers defined for {enum_value}."
                        )

                    cls._handlers[enum_value] = method
            except AttributeError:
                pass

        if unexpected := {key for key in cls._handlers if key not in enum}:
            raise InvalidEnumHandler(
                f"EnumHandler {cls.__name__} is parameterized with {enum} but has a "
                "handler registered for non-members of that enum: "
                + ", ".join(str(u) for u in unexpected)
            )

        if missing := {entry for entry in enum if entry not in cls._handlers}:
            raise InvalidEnumHandler(
                f"EnumHandler {cls.__name__} is not exhaustive over {enum.__name__}. "
                f"Missing entries: {', '.join(str(m) for m in missing)}"
            )

        if cache is CacheStrategy.EAGER_CACHE:
            for member in enum:
                cls(member)

    @classmethod
    def register(cls, *enum_values: M):
        """
        Registers a method as the handler for a given enum member or members.
        """
        if cls._final:
            raise RuntimeError(
                "You can't register an enum handler on a finalized class."
            )

        def _deco(fn: Callable[..., O]) -> Callable[..., O]:
            fn._handles = enum_values
            return fn

        return _deco


class InvalidEnumHandler(ValueError):
    pass


handles = EnumHandler.register
