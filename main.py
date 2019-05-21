from text_preprocessing import clean_text
from vocabulary import build_vocabulary, known_words, WORDS_NLTK
from spell_checker import SpellChecker


# Load training text
filepath = ''  # complete with the filepath where your data are
with open(filepath) as f:
    text = f.read()

# Clean text
text = clean_text(text)

# build vocabulary
WORDS = build_vocabulary(text)
KNOWN_WORDS = known_words(list(WORDS.keys()))

# Instantiate SpellChecker
spellchecker = SpellChecker(words=WORDS, known_words=KNOWN_WORDS)
spellchecker.spell_checking('helo')