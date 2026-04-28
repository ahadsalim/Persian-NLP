"""Tests for persian_nlp.Stemmer."""
import pytest
from persian_nlp import Stemmer


@pytest.fixture
def stemmer():
    return Stemmer()


class TestSuffixRemoval:
    def test_ha_plural(self, stemmer):
        assert stemmer.stem("کتابها") == "کتاب"

    def test_hay_plural_genitive(self, stemmer):
        assert stemmer.stem("کتابهای") == "کتاب"

    def test_superlative_tarin(self, stemmer):
        assert stemmer.stem("بزرگترین") == "بزرگ"

    def test_comparative_tar(self, stemmer):
        assert stemmer.stem("کوچکتر") == "کوچک"

    def test_animate_plural_an(self, stemmer):
        assert stemmer.stem("مردان") == "مرد"

    def test_nisba_ya(self, stemmer):
        assert stemmer.stem("ایرانی") == "ایران"

    def test_verbal_third_plural_nd(self, stemmer):
        assert stemmer.stem("می\u200cروند") == "می\u200cرو"


class TestNoChange:
    def test_short_word_unchanged(self, stemmer):
        """Word shorter than MIN_STEM_LEN after stripping → unchanged."""
        assert stemmer.stem("آب") == "آب"

    def test_word_without_suffix(self, stemmer):
        assert stemmer.stem("کتاب") == "کتاب"

    def test_empty_string(self, stemmer):
        assert stemmer.stem("") == ""


class TestZwnjHandling:
    def test_trailing_zwnj_stripped_from_stem(self, stemmer):
        """ZWNJ between stem and suffix must not remain in the result."""
        result = stemmer.stem("کتاب\u200cها")
        assert result == "کتاب"
        assert "\u200c" not in result
