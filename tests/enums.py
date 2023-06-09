from enum import Enum, auto

from enumhandler import CacheStrategy, EnumHandler


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


class CapitalContinents(EnumHandler, enum=Capitals):
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


class UncachedColorName(EnumHandler, enum=Colors, cache=CacheStrategy.NO_CACHE):
    @EnumHandler.register(Colors.RED)
    def red(self):
        return "Red"

    @EnumHandler.register(Colors.GREEN)
    def green(self):
        return "Green"

    @EnumHandler.register(Colors.BLUE)
    def blue(self):
        return "Blue"


class LazyCachedColorName(EnumHandler, enum=Colors, cache=CacheStrategy.LAZY_CACHE):
    @EnumHandler.register(Colors.RED)
    def red(self):
        return "Red"

    @EnumHandler.register(Colors.GREEN)
    def green(self):
        return "Green"

    @EnumHandler.register(Colors.BLUE)
    def blue(self):
        return "Blue"
