# <center> Naive spell checker </center>

In this repository, we implement a naive <b>spell checker</b> using a training corpus. That is, when fed with a mispelled word, the spell checker will output a list of correctly spelled candidate words. 


## Environment

It is recommended to use a virtual environment.

```bash
brew install python3
pip3 install --upgrade pip
pip3 install virtualenv
mkdir <project_name>
cd <project_name>
python3 -m venv <env_name>
source <env_name>/bin/activate
```

## Pre-requisites

You only need <b>nltk</b> (not included in a `requirements.txt` file here).

```python
pip3 install nltk==3.4.1
```

## Usage

The `main.py` script will walk the user through the utilization of this spell checker.
- The training corpus is a `.txt` file that is required to be loaded by the user. 
- We first clean it a bit (removing special characters, numbers, and putting everything to lowercase) using the `clean_text`function from the `text_preprocessing.py` script.
- From this training text, we construct a vocabulary with the help of the function `build_vocabulary` in the script `vocabulary.py`. As this vocabulary may contain unknown words, we extract the known words by intersecting it with a huge vocabulary loaded from `nltk`.
- The spell checker can then be used by provided it with a word for which we want to know if it is mispelled. If it is indeed mispelled, a list of candidate words is provided to the user. 

```python
text = clean_text(text)  # preprocess text

WORDS = build_vocabulary(text)  # build vocabulary from training corpus
KNOWN_WORDS = known_words(list(WORDS.keys()))  # build restricted vocabulary

spellchecker = SpellChecker(words=WORDS, known_words=KNOWN_WORDS)
spellchecker.spell_checking('helo').
```

## Details on the implementation of the Spell Checker

When fed with a new word, the spell checker first look if it is part of a huge reliable vocabulary (here, we use a vocabulary loaded from nltk). If it is, a string stating the word is correctly spelled is returned.

If the word is not part of the nltk vocabulary, the spell checker provides a list of potential candidates. To this end :
- it first generates a list of words whose <b>Levensthein distance</b> is exactly 1 from the word of interest (see method `generate_words`).
- it then select generated words that are part of a restricted vocabulary (defined as the correct words from our training corpus). 
- eventually, it returns a list of these words sorted by their occurrence in the training corpus, so that the first word of the list is the word getting the highest probability (see `probability` method). 

##### Levensthein distance
The Leveinsthein distance is a metric that we use to compare two strings together. It is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other. See [wikipedia](https://en.wikipedia.org/wiki/Levenshtein_distance).


## Author

* **Robin Beaudet** - *Initial work* - [github](https://github.com/RBeaudet)
