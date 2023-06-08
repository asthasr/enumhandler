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
            @handles(Colors.RED)
            def red(self):
                return "red"

            @handles(Colors.GREEN)
            def blue(self):
                return "blue"


def test_incorrect_enum_members_fail():
    with pytest.raises(InvalidEnumHandler):

        class _(EnumHandler, enum=Colors):
            @handles(Colors.RED, Colors.GREEN, Colors.BLUE)
            def color(self):
                return "color"

            @handles(Capitals.TOKYO)
            def city(self):
                return "city"


def test_duplicate_definitions_fail():
    with pytest.raises(InvalidEnumHandler):

        class _(EnumHandler, enum=Colors):
            @handles(Colors.RED, Colors.GREEN, Colors.BLUE)
            def color(self):
                return "color"

            @handles(Colors.RED)
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


def test_correct_definitions_work():
    class Continents(EnumHandler, enum=Capitals):
        @handles(Capitals.AMSTERDAM, Capitals.LONDON, Capitals.MOSCOW, Capitals.PARIS)
        def europe(self):
            return "Europe"

        @handles(Capitals.WASHINGTON_DC)
        def north_america(self):
            return "North America"

        @handles(Capitals.HANOI, Capitals.TOKYO)
        def asia(self):
            return "Asia"

        @handles(Capitals.CANBERRA)
        def australia(self):
            return "Australia"

    for entry in Capitals:
        assert Continents(entry)() == EXPECTED_CONTINENTS[entry]
