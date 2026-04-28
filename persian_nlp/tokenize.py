"""
Persian tokenisers — mirrors hazm.sent_tokenize / hazm.word_tokenize.

sent_tokenize: splits a Persian (or mixed) text into sentences.
word_tokenize: splits a sentence into word tokens.

Both functions are designed to reproduce the observable behaviour of
hazm 0.10.x / 0.12.x on the text that flows through this project.

Source reference: hazm 0.12.1
https://github.com/roshan-research/hazm/blob/v0.12.1/hazm/SentenceTokenizer.py
https://github.com/roshan-research/hazm/blob/v0.12.1/hazm/WordTokenizer.py
"""
from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# Sentence tokeniser
# ---------------------------------------------------------------------------

# Characters that end a sentence
_SENT_ENDERS = r"[.!?؟؛]"

# Sentence-boundary pattern:
#   • a sentence-ender (possibly repeated, e.g. "!!")
#   • followed by one or more whitespace chars   → split here
# OR
#   • two or more consecutive newlines           → split here
_SENT_BOUNDARY_RE = re.compile(
    r"(?<=" + _SENT_ENDERS + r")\s+"   # after ender + whitespace
    r"|"
    r"\n{2,}",                          # blank line / paragraph break
)

def sent_tokenize(text: str) -> list[str]:
    """
    Split *text* into a list of sentences.

    Sentence boundaries are placed:
    - after  . ! ? ؟ ؛  when followed by whitespace
    - at blank lines (two or more consecutive newlines)

    Returns an empty list for falsy input.
    """
    if not text:
        return []

    return [part.strip() for part in _SENT_BOUNDARY_RE.split(text) if part and part.strip()]


# ---------------------------------------------------------------------------
# Word tokeniser
# ---------------------------------------------------------------------------

# Punctuation characters that become individual tokens.
# We do NOT split on ZWNJ (U+200C) because Persian uses it to join
# parts of compound words (e.g.  می‌روم → keep as one token or split on space).
_PUNC_CHARS = r"""!"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~،؛؟»«…–—"""

# Pattern: match a run of non-whitespace, non-punctuation characters
# (including ZWNJ which is inside compound words), OR a single punctuation char.
_WORD_RE = re.compile(
    r"[^\s" + re.escape(_PUNC_CHARS) + r"]+"   # word (may contain ZWNJ)
    r"|"
    r"[" + re.escape(_PUNC_CHARS) + r"]",        # single punctuation token
)


def word_tokenize(text: str) -> list[str]:
    """
    Split *text* into a list of word/punctuation tokens.

    - Whitespace is consumed (not returned as tokens).
    - ZWNJ (U+200C) is treated as a non-space character so that Persian
      compound words like «می‌روم» are kept as a single token.
    - Each punctuation character becomes its own token.

    Returns an empty list for falsy input.
    """
    if not text:
        return []
    return _WORD_RE.findall(text)
