"""Tests for persian_nlp.Normalizer."""
import pytest
from persian_nlp import Normalizer


@pytest.fixture
def normalizer():
    """Default normalizer — mirrors project settings (persian_numbers=False, correct_spacing=False)."""
    return Normalizer(persian_numbers=False, correct_spacing=False)


@pytest.fixture
def normalizer_full():
    """Normalizer with all options enabled."""
    return Normalizer(persian_numbers=True, correct_spacing=True)


class TestCharacterSubstitution:
    def test_arabic_kaf_to_persian_kaf(self, normalizer):
        assert normalizer.normalize("كتاب") == "کتاب"

    def test_arabic_ya_to_persian_ya(self, normalizer):
        assert normalizer.normalize("يك") == "یک"

    def test_alef_maqsura_to_persian_ya(self, normalizer):
        assert normalizer.normalize("موسى") == "موسی"

    def test_mixed_arabic_chars(self, normalizer):
        assert normalizer.normalize("يك كتاب فارسي") == "یک کتاب فارسی"


class TestDiacritics:
    def test_harakat_removed(self, normalizer):
        assert normalizer.normalize("كُتُب") == "کتب"

    def test_fathatan_removed(self, normalizer):
        assert normalizer.normalize("أَحسَن") == "أحسن"


class TestTatweel:
    def test_kashida_removed(self, normalizer):
        assert "ـ" not in normalizer.normalize("اسلاـم")

    def test_multiple_tatweel(self, normalizer):
        result = normalizer.normalize("سلاـاـاـم")
        assert "ـ" not in result


class TestZeroWidthChars:
    def test_zwnj_becomes_space(self, normalizer):
        result = normalizer.normalize("متن\u200cفارسی")
        assert "\u200c" not in result

    def test_zwj_becomes_space(self, normalizer):
        result = normalizer.normalize("کلمه\u200dکلمه")
        assert "\u200d" not in result

    def test_directional_marks_removed(self, normalizer):
        result = normalizer.normalize("سلام\u200e دنیا\u200f")
        assert "\u200e" not in result
        assert "\u200f" not in result


class TestPersianNumbers:
    def test_arabic_indic_kept_when_disabled(self, normalizer):
        """arabic-indic digits stay as-is when persian_numbers=False."""
        result = normalizer.normalize("١٢٣")
        assert result == "١٢٣"

    def test_arabic_indic_to_persian_when_enabled(self, normalizer_full):
        """arabic-indic digits converted to Persian when persian_numbers=True."""
        result = normalizer_full.normalize("١٢٣")
        assert result == "۱۲۳"


class TestWhitespace:
    def test_multiple_spaces_collapsed(self, normalizer):
        assert normalizer.normalize("سلام   دنیا") == "سلام دنیا"

    def test_leading_trailing_stripped(self, normalizer):
        assert normalizer.normalize("  سلام  ") == "سلام"

    def test_empty_string(self, normalizer):
        assert normalizer.normalize("") == ""

    def test_none_like_empty(self, normalizer):
        assert normalizer.normalize("") == ""


class TestCorrectSpacing:
    def test_space_before_punc_removed(self, normalizer_full):
        assert normalizer_full.normalize("سلام ،") == "سلام،"

    def test_spacing_preserved_when_disabled(self, normalizer):
        """correct_spacing=False — punctuation spacing unchanged."""
        assert normalizer.normalize("سلام ،") == "سلام ،"
