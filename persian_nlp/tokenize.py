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

# Pattern to detect numeric context "1.5", "2.3" etc. — avoid splitting there.
# We post-process and re-join fragments that were incorrectly split.
_NUMBER_SPLIT_RE = re.compile(r"^\d+$")


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

    parts = _SENT_BOUNDARY_RE.split(text)

    sentences: list[str] = []
    i = 0
    while i < len(parts):
        fragment = parts[i].strip()
        if not fragment:
            i += 1
            continue

        # Re-join if the split happened inside a decimal number like "1.5"
        # hazm exhibits the same conservative behaviour.
        if (
            i + 1 < len(parts)
            and fragment
            and fragment[-1] == "."
            and _NUMBER_SPLIT_RE.match(fragment[:-1])  # "1" before the "."
        ):
            merged = fragment + parts[i + 1].strip()
            sentences.append(merged)
            i += 2
            continue

        sentences.append(fragment)
        i += 1

    return sentences


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
