import pytest

from enumhandler import EnumHandler, InvalidEnumHandler, handles

from .enums import CapitalContinents, Capitals, Colors


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


def test_correct_definitions_work():
    for entry in Capitals:
        assert CapitalContinents(entry)() == EXPECTED_CONTINENTS[entry]


def test_registering_another_handler_fails():
    with pytest.raises(RuntimeError):
        CapitalContinents.register(Capitals.AMSTERDAM)


def test_using_reexported_handles_works():
    class ColorHandler(EnumHandler, enum=Colors):
        @handles(Colors.RED, Colors.GREEN, Colors.BLUE)
        def is_color(self):
            return True

    assert ColorHandler(Colors.BLUE)()
