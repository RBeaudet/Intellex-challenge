from collections import Counter
from vocabulary import WORDS_NLTK


class SpellChecker():

    def __init__(self, words, known_words):
        """
        This class allows to check the spelling of a word given
        a training corpus `text`. For checking if a word is
        correctly spelled, the user enter the word `word`. If the
        word does not exist, a list of candidates for this word is 
        returned.

        Arguments:
        - words : (Counter) Vocabulary generated from a training corpus.
        - known_words : (Set) Vocabulary generated from a training corpus, intersected 
          with vocabulary from NLTK. `WORDS`thus represents all the known words
          from the training corpus.
        """
        self.WORDS = words
        self.WORDS_NLTK = WORDS_NLTK
        self.KNOWN_WORDS = known_words

        assert isinstance(self.WORDS, Counter)
        assert isinstance(self.WORDS_NLTK, list)
        assert isinstance(self.KNOWN_WORDS, set)


    def probability(self, word):
        """
        Compute probability of word `word` based on its
        occurrence in the training corpus.

        Arguments :
        - word : (str) the word for which we wish to compute the probability.

        Output:
        - prob : (float) number between 0 and 1 representing the probability 
          associated to the word.
        """
        N = sum(self.WORDS.values())  # total number of words in training corpus
        prob = self.WORDS[word] / N  # nb_occurrences / total_nb_words
        return prob

        
    def generate_words(self, word):
        """
        From a string 'word', generates strings that are at
        Leveinsthein distance 1 from 'word'. To do this, we 
        manually perform every operation needed to generate
        new words.

        Arguments :
        - word : (str) the word from which to generate candidates.

        Output:
        - A list of all new strings that are at Levensthein distance
          1 from the word `word`.
        """
        # letters in the alphabet
        letters = 'abcdefghijklmnopqrstuvwxyz'
        
        # split word at each position. For instance, "hello" will yield
        # ('', 'hello'), ('h', 'ello'), ('he', 'llo'), etc.
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        
        # For each above split, delete one letter. We have
        # 'ello', 'hllo', 'helo', 'helo', 'hell'
        deletes = [L + R[1:] for L, R in splits if R]
        
        # For each split, transpose letters. We have
        # 'ehllo', 'hlelo', 'hello', 'helol'
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        
        # For each split, replace a letter by one letter from the alphabet
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        
        # For each split, insert a letter from the alphabet
        inserts = [L + c + R for L, R in splits for c in letters]
        
        return set(deletes + transposes + replaces + inserts)


    def spell_checking(self, word):
        """
        Main function of our spell checker,
        to see if a word specified by user is spelled correctly.

        Arguments :
        - word (str) : the word being tested

        Output:
        - If the word is spelled correctly, outputs a string. If
          the word does not exist, outputs a list of candidates for
          this word.
        """
        
        # Convert to lowercase
        word = word.lower()
        
        # Check if word is known
        if word in self.WORDS_NLTK:
            return "The word is correctly spelled."
        
        # Otherwise, generate candidate words
        else:
            print("This word is unknown.")
            corrected_words = []  # list that hosts potentiel words
            candidates = self.generate_words(word)  # list of candidate words
            
            for candidate in candidates:
                if candidate in self.KNOWN_WORDS:
                    corrected_words.append(candidate)

            if len(corrected_words) > 0:
                corrected_words = sorted(corrected_words, key=self.probability)
                return corrected_words
            else:
                return "Impossible to provide candidate words :("