from enum import Enum, auto

import pytest

from enumhandler import EnumHandler, InvalidEnumHandler, handles


class Colors(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class Capitals(Enum):
    AMSTERDAM = auto()
    CANBERRA = auto()
    HANOI = auto()
    LONDON = auto()
    MOSCOW = auto()
    PARIS = auto()
    TOKYO = auto()
    WASHINGTON_DC = auto()


def test_non_exhaustive_definitions_fail():
    with pytest.raises(InvalidEnumHandler):

        class _(EnumHandler, enum=Colors):
            @EnumHandler.register(Colors.RED)
            def red(self):
                return "red"

            @EnumHandler.register(Colors.GREEN)
            def blue(self):
                return "blue"


def test_incorrect_enum_members_fail():
    with pytest.raises(InvalidEnumHandler):

        class _(EnumHandler, enum=Colors):
            @EnumHandler.register(Colors.RED, Colors.GREEN, Colors.BLUE)
            def color(self):
                return "color"

            @EnumHandler.register(Capitals.TOKYO)
            def city(self):
                return "city"


def test_duplicate_definitions_fail():
    with pytest.raises(InvalidEnumHandler):

        class _(EnumHandler, enum=Colors):
            @EnumHandler.register(Colors.RED, Colors.GREEN, Colors.BLUE)
            def color(self):
                return "color"

            @EnumHandler.register(Colors.RED)
            def city(self):
                return "duplicate"


EXPECTED_CONTINENTS = {
    Capitals.AMSTERDAM: "Europe",
    Capitals.CANBERRA: "Australia",
    Capitals.HANOI: "Asia",
    Capitals.LONDON: "Europe",
    Capitals.MOSCOW: "Europe",
    Capitals.PARIS: "Europe",
    Capitals.TOKYO: "Asia",
    Capitals.WASHINGTON_DC: "North America",
}


@pytest.fixture
def valid_handler():
    class Continents(EnumHandler, enum=Capitals):
        @EnumHandler.register(
            Capitals.AMSTERDAM, Capitals.LONDON, Capitals.MOSCOW, Capitals.PARIS
        )
        def europe(self):
            return "Europe"

        @EnumHandler.register(Capitals.WASHINGTON_DC)
        def north_america(self):
            return "North America"

        @EnumHandler.register(Capitals.HANOI, Capitals.TOKYO)
        def asia(self):
            return "Asia"

        @EnumHandler.register(Capitals.CANBERRA)
        def australia(self):
            return "Australia"

    return Continents


def test_correct_definitions_work(valid_handler):
    for entry in Capitals:
        assert valid_handler(entry)() == EXPECTED_CONTINENTS[entry]


def test_registering_another_handler_fails(valid_handler):
    with pytest.raises(RuntimeError):
        valid_handler.register(Capitals.AMSTERDAM)


def test_using_reexported_handles_works():
    class ColorHandler(EnumHandler, enum=Colors):
        @handles(Colors.RED, Colors.GREEN, Colors.BLUE)
        def is_color(self):
            return True

    assert ColorHandler(Colors.BLUE)()
