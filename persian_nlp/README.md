# persian_nlp

Minimal standalone Persian NLP library for this project.  
**Python 3.8+ compatible. No external dependencies.**

Replaces the `hazm` library (incompatible with Python 3.11 in v0.12+) by
re-implementing only the features actually used in the codebase.

## Public API

```python
from persian_nlp import Normalizer, Stemmer, sent_tokenize, word_tokenize
```

### `Normalizer`

```python
normalizer = Normalizer(persian_numbers=False, correct_spacing=False)
text = normalizer.normalize("كتاب‌هاي فارسي")
# → "کتاب های فارسی"
```

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `persian_numbers` | bool | `True` | Convert Arabic-Indic digits (٠-٩) to Persian digits (۰-۹) |
| `correct_spacing` | bool | `True` | Adjust spacing around punctuation |

**What it does**

- Removes diacritics (harakat)
- Removes tatweel / kashida (ـ)
- Converts Arabic ya (ي) and kaf (ك) to their Persian equivalents (ی, ک)
- Removes directional marks (LRM/RLM) and converts ZWNJ/ZWJ to space
- Removes control characters
- NFC Unicode normalisation
- Collapses multiple spaces

### `Stemmer`

```python
stemmer = Stemmer()
print(stemmer.stem("کتاب‌ها"))   # → کتاب
print(stemmer.stem("بزرگترین"))  # → بزرگ
```

Suffix-stripping stemmer. Returns the word unchanged if no suffix matches or
if removing the suffix would leave fewer than 2 characters.

### `sent_tokenize`

```python
sentences = sent_tokenize("جمله اول. جمله دوم؟ جمله سوم!")
# → ["جمله اول.", "جمله دوم؟", "جمله سوم!"]
```

Splits text on `.`, `!`, `?`, `؟`, `؛` followed by whitespace, and on blank
lines (paragraph breaks).

### `word_tokenize`

```python
words = word_tokenize("سلام، دنیا!")
# → ["سلام", "،", "دنیا", "!"]
```

Splits text into word and punctuation tokens.  
ZWNJ (U+200C) is treated as a non-space character so Persian compound words
(e.g. `می‌روم`) remain as a single token.

## Extending

Each module (`normalizer.py`, `stemmer.py`, `tokenize.py`) is independent and
can be imported directly.  Add new suffixes to `stemmer.SUFFIXES` or adjust
the regex patterns in `tokenize.py` as needed.
