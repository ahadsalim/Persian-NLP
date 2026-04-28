"""
Persian stemmer — mirrors hazm.Stemmer.

Implements a simple suffix-stripping stemmer for Persian.  Only the
``stem(word)`` method is used by this project.

The suffix list and ordering follow hazm 0.10.x / 0.12.x so that the
output stays consistent with historical behaviour.

Source reference:
https://github.com/roshan-research/hazm/blob/v0.12.1/hazm/Stemmer.py
"""
from __future__ import annotations


# Suffixes are tried longest-first; the first match whose removal leaves
# a stem of at least MIN_STEM_LEN characters is applied.
MIN_STEM_LEN = 2

SUFFIXES: list[str] = [
    # Derivational / inflectional suffixes (longest first)
    "ترین",   # superlative
    "های",    # plural + genitive ya
    "گیری",   # verbal noun suffix
    "پذیری",
    "پذیر",
    "گری",
    "گر",
    "یها",
    "ها",     # plural
    "تر",     # comparative
    "ان",     # animate plural / agent
    "ات",     # Arabic broken plural
    # Verbal personal endings
    "یم",     # 1st pl.
    "ید",     # 2nd pl.
    "ند",     # 3rd pl.
    "م",      # 1st sg.
    "ت",      # 2nd sg.
    "د",      # 3rd sg.
    # Nominal / adjectival suffixes (must come after verbal ones)
    "ی",      # nisba / indefinite ya
]


class Stemmer:
    """
    Stem a single Persian word by removing the longest matching suffix.

    Usage::

        stemmer = Stemmer()
        print(stemmer.stem("کتاب‌ها"))   # → کتاب
    """

    def stem(self, word: str) -> str:
        """Return the stem of *word*, or *word* unchanged if no suffix matches."""
        if not word:
            return word

        for suffix in SUFFIXES:
            if word.endswith(suffix):
                # Strip suffix and any trailing ZWNJ/whitespace left behind
                candidate = word[: -len(suffix)].rstrip("\u200c\u200d ")
                if len(candidate) >= MIN_STEM_LEN:
                    return candidate

        return word
