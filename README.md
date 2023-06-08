# EnumHandler

If you're like me, you were disappointed to see that structural pattern matching ([PEP 622]) landed in Python without any of the proposed exhaustiveness guarantees ([PEP 634]).
Although `match` and `case` are still useful, exhaustive matching over an enum is a comfortable idiom in other languages, and I was looking forward to first-class treatment of this in Python.
Worse, I ended up writing a number of repetitive exhaustiveness tests:

```python
import pytest

from myproject import Colors, name_of_color

@pytest.parametrize(MyEnum)
def test_name_of_color_exhaustiveness(value):
    assert name_of_color(value)
```

Tests that don't care about the return value of the function under test are a hallmark of type system failures.

This library fixes that by providing a base class for classes that exhaustively cover an enumeration.
Upon class definition, `EnumHandler` will validate the exhaustiveness and uniqueness of handlers registered on any subclass using the `EnumHandler.register` decorator.

```python
from enum import Enum, auto

from enumhandler import EnumHandler, handles


class Colors(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class NameOfColor(EnumHandler, enum=Colors):
    @handles(Colors.RED)
    def red(self) -> str:
        return "Red"

    @handles(Colors.GREEN)
    def green(self) -> str:
        return "Green"

    @handles(Colors.BLUE)
    def blue(self) -> str:
        return "Blue"
```

The class is instantiated with a member of the enum, and the resulting instance is callable:

```pycon
>>> print(NameOfColor(Colors.RED)())
Red
```

An `InvalidEnumHandler` exception is raised in three cases:

- Not all enum values are handled.
- One enum value has multiple registered handlers.
- A handler is registered for the incorrect enum.
- A handler is registered on an existing class.

Please note that subclassing is currently not supported.

[PEP 622]: https://peps.python.org/pep-0622/
[PEP 634]: https://peps.python.org/pep-0634/
