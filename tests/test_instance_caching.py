import pytest

from enumhandler import CacheStrategy, EnumHandler

from .enums import CapitalContinents, Capitals, Colors, UncachedColorName


@pytest.mark.parametrize("capital", Capitals)
def test_instances_cached_eagerly_by_default(capital):
    left = CapitalContinents(capital)
    right = CapitalContinents(capital)
    assert left() == right()
    assert left is right


def test_instances_cached_lazily():
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

    assert LazyCachedColorName._instance_cache == {}

    for n, color in enumerate(Colors):
        assert len(LazyCachedColorName._instance_cache) == n
        assert LazyCachedColorName(color) is LazyCachedColorName(color)

    assert len(LazyCachedColorName._instance_cache) == len(Colors)


@pytest.mark.parametrize("color", Colors)
def test_instances_not_cached_for_no_caching_strategy(color):
    left = UncachedColorName(color)
    right = UncachedColorName(color)
    assert left is not right
