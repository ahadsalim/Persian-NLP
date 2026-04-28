"""
persian_nlp — Minimal standalone Persian NLP library.

A drop-in replacement for the hazm functions used in this project,
compatible with Python 3.11+ and any NumPy 1.x / 2.x version.

Public API mirrors the subset of hazm actually used here:

    from persian_nlp import Normalizer, Stemmer, sent_tokenize, word_tokenize

    normalizer = Normalizer(persian_numbers=False, correct_spacing=False)
    text = normalizer.normalize(raw_text)

    stemmer = Stemmer()
    stem = stemmer.stem(word)

    sentences = sent_tokenize(text)
    words     = word_tokenize(sentence)
"""

from .normalizer import Normalizer
from .stemmer import Stemmer
from .tokenize import sent_tokenize, word_tokenize

__all__ = ["Normalizer", "Stemmer", "sent_tokenize", "word_tokenize"]
__version__ = "1.0.0"
