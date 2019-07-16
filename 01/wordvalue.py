from data import DICTIONARY, LETTER_SCORES

def load_words(path=DICTIONARY):
    """Load dictionary into a list and return list"""
    word_list = []
    with open(path) as dic:
        word_list = dic.read().split()
    return word_list

def calc_word_value(word):
    """Calculate the value of the word entered into function
    using imported constant mapping LETTER_SCORES"""
    word = word.upper()
    score = 0
    for letter in word:
        try:
            score += LETTER_SCORES[letter]
        except KeyError:
            pass
    return score

def max_word_value(words=None):
    """Calculate the word with the max value, can receive a list
    of words as arg, if none provided uses default DICTIONARY"""
    if words == None:
        words = load_words()
    previous_best_score = 0
    previous_best_word = ""
    for word in words:
        score = calc_word_value(word)
        if score > previous_best_score:
            previous_best_word = word
            previous_best_score = score
    return previous_best_word

if __name__ == "__main__":
    words = load_words(DICTIONARY)
    word = max_word_value(words)
    print(f"The word with the highest possible score in english is {word}!")
