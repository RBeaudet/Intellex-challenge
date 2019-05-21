import re
from collections import Counter
import nltk
from nltk.corpus import words
nltk.download('words')

special_char_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:],')
number_regex = re.compile('[0-9]')


class SpellChecker():

    def __init__(self, filepath):
        """
        This class allows to check the spelling of a word given
        a training corpus loaded from `filepath`.

        Arguments:
        - filepath : (str) filepath from where to load the training corpus
        """

        self.filepath = filepath
        self._load()


    def _load(self):
        """
        Load data, and build vocabulary from training corpus and NLTK.
        """
        # Load text
        with open(self.filepath) as f:
            text = f.read()
            self.text = self._clean_text(text)

        # build vocabulary
        self.WORDS = Counter(self._words(self.text))
        self.WORDS_NLTK = words.words()


    def _clean_text(self, text):
        """
        Clean text from special characters and numbers, and put it in lowercase.

        Arguments:
        - text (str) : the input text

        Output:
        - A string with tghe preprocessed text
        """
        new_text = []
        
        for word in text.split():
            word = word.lower()  # lowercase
            word = re.sub(special_char_regex, '', word)  # remove special chartacters
            word = re.sub(number_regex, '', word)  # remove numbers
            
            # append in new_text
            new_text.append(word)
        
        return ' '.join(new_text)

    
    def _words(self, text):
        """ 
        Find words in a text. 
        """ 
        return re.findall(r'\w+', text)


    def probability(self, word, N=sum(self.WORDS.values())):
        """
        Compute probability of word 'word' based on its
        occurrence in the corpus.

        Arguments :
        - word (str) : word of interest
        - N (int) : total number of words in the corpus
        """
        prob = self.WORDS[word] / N
        return prob

        
    def generate_words(self, word):
        """
        From a string 'word', generates strings that are at
        Leveinsthein distance 1 from 'word'. To do this, we 
        manually perform every operation needed to generate
        new words.

        Arguments :
        - word (str) : the word from which to generate

        Output:
        - A list of all new words
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
            return "Word correctly spelled"
        
        # Otherwise, generate words with Levensthein distance 1 from that word
        else:
            print("Unknown word")
            new_words = []  # list that hosts potentiel words
            candidates = self.generate_words(word)
            
            for candidate in candidates:
                if candidate in self.WORDS_NLTK:
                    new_words.append(candidate)
            
            # Now that we have our candidate words, take the one that appears
            # the most in our corpus
            final_words = []  # final list of words
            for w in new_words:
                # check that w is in our corpus
                if w in self.WORDS: 
                    final_words.append(w)
                    final_words = sorted(final_words, key=self.probability)
            
            # If no candidate word is in our corpus, output initial candiate words
            if len(final_words) == 0:
                return new_words
            else:
                return final_words