"""Tests for persian_nlp.sent_tokenize and word_tokenize."""
import pytest
from persian_nlp import sent_tokenize, word_tokenize


class TestSentTokenize:
    def test_period_split(self):
        result = sent_tokenize("جمله اول. جمله دوم.")
        assert result == ["جمله اول.", "جمله دوم."]

    def test_question_mark_split(self):
        result = sent_tokenize("سوال اول؟ سوال دوم؟")
        assert result == ["سوال اول؟", "سوال دوم؟"]

    def test_exclamation_split(self):
        result = sent_tokenize("اول! دوم!")
        assert result == ["اول!", "دوم!"]

    def test_persian_question_mark(self):
        result = sent_tokenize("چه کسی آمد؟ نمی‌دانم.")
        assert len(result) == 2

    def test_semicolon_split(self):
        result = sent_tokenize("اول؛ دوم.")
        assert len(result) == 2

    def test_paragraph_break(self):
        result = sent_tokenize("بند اول.\n\nبند دوم.")
        assert len(result) == 2

    def test_empty_string(self):
        assert sent_tokenize("") == []

    def test_single_sentence(self):
        result = sent_tokenize("یک جمله بدون خاتمه")
        assert result == ["یک جمله بدون خاتمه"]

    def test_mixed_punctuation(self):
        result = sent_tokenize("اول. دوم؟ سوم!")
        assert result == ["اول.", "دوم؟", "سوم!"]

    def test_whitespace_not_in_tokens(self):
        for sent in sent_tokenize("اول. دوم. سوم."):
            assert sent == sent.strip()


class TestWordTokenize:
    def test_basic_split(self):
        result = word_tokenize("سلام دنیا")
        assert result == ["سلام", "دنیا"]

    def test_punctuation_as_tokens(self):
        result = word_tokenize("سلام، دنیا!")
        assert "سلام" in result
        assert "،" in result
        assert "دنیا" in result
        assert "!" in result

    def test_zwnj_kept_inside_compound(self):
        """ZWNJ within a compound word must not split the word."""
        result = word_tokenize("می\u200cروم")
        assert "می\u200cروم" in result

    def test_empty_string(self):
        assert word_tokenize("") == []

    def test_no_empty_tokens(self):
        for token in word_tokenize("  سلام   دنیا  "):
            assert token.strip() != ""

    def test_period_as_token(self):
        result = word_tokenize("جمله.")
        assert "جمله" in result
        assert "." in result

    def test_guillemets(self):
        result = word_tokenize("«متن»")
        assert "«" in result
        assert "متن" in result
        assert "»" in result
