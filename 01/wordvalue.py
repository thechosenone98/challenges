from data import DICTIONARY, LETTER_SCORES

def load_words(path):
    """Load dictionary into a list and return list"""
    word_list = []
    with open(path) as dic:
        word_list = dic.read().upper().split()
    return word_list

def calc_word_value(word):
    """Calculate the value of the word entered into function
    using imported constant mapping LETTER_SCORES"""
    score = 0
    for letter in word:
        try:
            score += LETTER_SCORES[letter]
        except KeyError:
            pass
    return score

def max_word_value(words):
    """Calculate the word with the max value, can receive a list
    of words as arg, if none provided uses default DICTIONARY"""
    previous_best_score = 0
    previous_best_word = ""
    for word in words:
        score = calc_word_value(word)
        if score > previous_best_score:
            previous_best_word = word
    return (word, score)

if __name__ == "__main__":
    words = load_words(DICTIONARY)
    word, highest_score = max_word_value(words)
    print(f"The word with the highest score is {word} with an outstanding {highest_score} points!")
