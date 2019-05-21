import nltk
nltk.download('punkt')  # download punctuation kit


def clean_text(text):
    """
    This function takes a written text and performs
    a naive preprocessing step, removing special characters,
    numbers, or putting everything to lowercase.

    Arguments:
    - text : a string containing the text to be cleaned.

    Output:
    - clean_text : the cleaned text.
    """
    text = ''.join([i for i in text if not i.isdigit()])  # remove number
    words = nltk.word_tokenize(text)  # tokenize text into a list of words
    words = [word.lower() for word in words if word.isalpha()]  # remove special characters
    clean_text = ' '.join(words)  # transform back into a string

    return clean_text


# SANITY CHECK

def clean_text_sanity_check():
    """
    Check function with a simple example.
    """
    text1 = "My, name3 : is Robin!"
    text2 = "my name is robin"
    assert clean_text(text1) == text2