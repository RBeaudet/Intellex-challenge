import re
from collections import Counter
import nltk
from nltk.corpus import words
nltk.download('words')


# vocabulary loaded from NLTK
WORDS_NLTK = words.words()  


def build_vocabulary(text):
    """
    This function is called when instanciating the class, and 
    constructs the vocabulary from the training corpus.
    The vocabulary takes the form of a dictionary where a key is
    a word, and the value is the number of occurrences of this word.

    Arguments:
    - text : (str) The corpus from which to build a custom vocabulary.

    Returns:
    - WORDS : (Counter) a dictionary mapping a word to its occurrence.
    """
    words = re.findall(r'\w+', text)  # transform text into a list of words
    WORDS = Counter(words)
    return WORDS


def known_words(words):
    """
    From a training vocabulary `words` which might
    contain mispelled words, extract a subset of words
    that are for sure correctly spelled. To do this,
    we intersect the words from `text` with the
    vocabulary loaded from NLTK.

    Arguments:
    - words : A list of words constituting a training corpus vocabulary.

    Returns:
    - A set object of all the known words from the vocabulary `words`.
    """
    return set(w for w in words if w in WORDS_NLTK)


# SANITY CHECKS

def build_vocabulary_sanity_check():
    """
    Sanity check in order to check that the function is working
    with a simple example.
    """
    text = "hello hello goodbye"
    vocabulary = build_vocabulary(text)
    assert isinstance(vocabulary, Counter)
    assert len(list(vocabulary.keys())) == 2
    assert vocabulary["hello"] == 2
    assert vocabulary["goodbye"] == 1


def known_words_sanity_check():
    """
    Sanity check in order to check that the function is working
    with a simple example.
    """
    text = ["hello", "helo", "bye"]
    result = known_words(text)
    assert isinstance(result, set)
    assert 'helo' not in known_words