"""
Persian text normalizer — mirrors the behaviour of hazm.Normalizer.

Only the features actually exercised by this project are implemented:
    - Arabic → Persian character substitutions (ya, kaf, alef maqsura)
    - Tatweel (kashida) removal
    - ZWNJ / ZWJ cleanup
    - Control-character removal
    - Whitespace normalisation
    - Diacritic stripping
    - persian_numbers flag  (False = keep digits as-is)
    - correct_spacing flag  (False = no punctuation re-spacing)

Source reference: hazm 0.12.1
https://github.com/roshan-research/hazm/blob/v0.12.1/hazm/Normalizer.py
"""
from __future__ import annotations

import re
import unicodedata


# ---------------------------------------------------------------------------
# Character-level substitution tables
# ---------------------------------------------------------------------------

# Arabic → Persian equivalents
_ARABIC_TO_PERSIAN: dict[str, str] = {
    "\u0643": "\u06a9",   # ك Arabic kaf  → ک Persian kaf
    "\u064a": "\u06cc",   # ي Arabic ya   → ی Persian ya
    "\u0649": "\u06cc",   # ى Alef maqsura → ی
    "\u0626": "\u06cc",   # ئ (ya with hamza) mapped to Persian ya in some normalisers
}

# Persian/Arabic digit mapping (only used when persian_numbers=True)
_ARABIC_INDIC_TO_PERSIAN: dict[str, str] = {
    "\u0660": "\u06f0", "\u0661": "\u06f1", "\u0662": "\u06f2",
    "\u0663": "\u06f3", "\u0664": "\u06f4", "\u0665": "\u06f5",
    "\u0666": "\u06f6", "\u0667": "\u06f7", "\u0668": "\u06f8",
    "\u0669": "\u06f9",
}

# Diacritics (harakat) — always removed
_DIACRITICS_RE = re.compile(
    "[\u064b-\u065f\u0670]"   # fathatan … superscript alef
)

# Tatweel (kashida) — decorative elongation glyph
_TATWEEL = "\u0640"

# Zero-width characters that should become a plain space (or be dropped)
# U+200C = ZWNJ, U+200D = ZWJ, U+200E = LRM, U+200F = RLM
_ZW_SPACE_RE = re.compile("[\u200e\u200f]")   # directional marks → drop
_ZWNJ_RE = re.compile("[\u200c\u200d]")        # joiners → single space

# Whitespace normalisation: collapse any run of spaces/tabs to one space
_MULTI_SPACE_RE = re.compile(r" {2,}")

# Control characters (except ordinary whitespace \n \r \t)
_CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")


class Normalizer:
    """
    Normalise Persian text.

    Parameters
    ----------
    persian_numbers : bool
        If True, convert Arabic-Indic digits (٠-٩) to Extended Arabic-Indic
        (Persian) digits (۰-۹). Defaults to False (keep digits unchanged).
    correct_spacing : bool
        If True, adjust spacing around punctuation marks (add/remove spaces).
        Defaults to False (preserve spacing as-is).
    """

    def __init__(
        self,
        persian_numbers: bool = True,
        correct_spacing: bool = True,
    ) -> None:
        self.persian_numbers = persian_numbers
        self.correct_spacing = correct_spacing

        # Build a single translation table from all char substitutions.
        self._trans = str.maketrans(_ARABIC_TO_PERSIAN)

        if persian_numbers:
            self._trans.update(str.maketrans(_ARABIC_INDIC_TO_PERSIAN))

        if correct_spacing:
            # Pre-compiled patterns used when correct_spacing=True
            self._before_punc_re = re.compile(r"\s+([،؛:.!?؟»\)])")
            self._after_punc_re = re.compile(r"([«\(])\s+")

    # ------------------------------------------------------------------
    def normalize(self, text: str) -> str:
        """Return a normalised copy of *text*."""
        if not text:
            return ""

        # 1. Remove control characters
        text = _CTRL_RE.sub("", text)

        # 2. Drop directional marks; convert joiners to space
        text = _ZW_SPACE_RE.sub("", text)
        text = _ZWNJ_RE.sub(" ", text)

        # 3. Strip diacritics (harakat)
        text = _DIACRITICS_RE.sub("", text)

        # 4. Remove tatweel
        text = text.replace(_TATWEEL, "")

        # 5. Arabic → Persian character substitutions
        text = text.translate(self._trans)

        # 6. NFC normalisation (unify composed/decomposed forms)
        text = unicodedata.normalize("NFC", text)

        # 7. Collapse multiple spaces (never touch newlines)
        text = _MULTI_SPACE_RE.sub(" ", text)

        # 8. correct_spacing (optional)
        if self.correct_spacing:
            text = self._before_punc_re.sub(r"\1", text)
            text = self._after_punc_re.sub(r"\1", text)

        return text.strip()
