#!/usr/bin/python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

from data import DICTIONARY, LETTER_SCORES, POUCH
from random import sample
from itertools import permutations, chain
from collections import namedtuple
from datetime import datetime
import shelve
import sys

NUM_LETTERS = 7
Entry = namedtuple('Entry', ['draw', 'word', 'score', 'best_word', 'best_score'])

# re-use from challenge 01
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


# re-use from challenge 01
def max_word_value(words):
    """Calculate the word with the max value, can receive a list
    of words as arg, if none provided uses default DICTIONARY"""
    previous_best_score = 0
    previous_best_word = ""
    for word in words:
        score = calc_word_value(word)
        if score > previous_best_score:
            previous_best_word = word
            previous_best_score = score
    return previous_best_word

def _get_permutations_draw(draw):
    return chain.from_iterable([list(permutations(draw, n)) for n in range(1, NUM_LETTERS + 1)])

def get_possible_dict_words(draw):
    possible_word = []
    # Generate all permutation of length 1 to N
    for perm in _get_permutations_draw(draw):
        perm = "".join(perm).lower()
        if perm in DICTIONARY:
            possible_word.append(perm)
    return possible_word

def draw_letters(amount=None):
    if amount == None:
        amount = 7
    return sample(POUCH, amount)

def display_draw(draw):
    return " ".join([letter.upper() for letter in draw])

def _validation(word, draw):
    if set(word).issubset(draw):
        if word.lower() in get_possible_dict_words(draw):
            return True
        else:
            raise ValueError("The word you typed does not exist.")
    raise ValueError("The word you type contains letters that you do not possess.")

def main():
    if sys.argv[1] == "play":
        draw = draw_letters()
        print(f"Here are the letters you drew : {display_draw(draw)}")
        print("Try and make the best score you can!")
        word = ""
        while True:
            word = input("Please enter a word composed of the letters above (you can only use each letter once) : \n")
            try:
                if _validation(word, draw):
                    break
            except ValueError as e:
                print(e)

        score = calc_word_value(word)
        # This redundancy is cause by the fact that test_game expect only the best word to come back from max_word_value...
        # By redudancy I mean that the score of the best word has been calculated but not returned inside the max_word_value function
        # Hence we need to recalculate it...
        best_word = max_word_value(get_possible_dict_words(draw))
        max_score = calc_word_value(best_word)
        print(f"You scored {score} points with the word {word.upper()}")
        print(f"The maximum score you could have had with these letter is {max_score} using the word {best_word.upper()}")

        # Check if this score is th greatest yet and store it
        # Also store the draw and the word you wrote
        with shelve.open("SCRABBLEPY", "c") as db:
            if 'high_score' in db:
                if max_score > db['high_score']:
                    db['high_score'] = score
            else:
                db['high_score'] = score
            # Store the draw, the word, the score, the best word and the best score possible with a timestamp
            db[datetime.now().strftime("%Y/%m/%d    %H:%M:%S")] = Entry(draw, word.upper(), score, best_word.upper(), max_score)
    elif sys.argv[1] == "list":
        with shelve.open("SCRABBLEPY") as db:
            for key in sorted(db.keys()):
                if key == 'high_score':
                    print(f"Your high score is {db[key]}")
                    continue
                else:
                    #Print the date (keys are dates expect for high_score)
                    print(key)
                    print(f"DRAW : {db[key].draw}")
                    print(f"USER WORD : {db[key].word}")
                    print(f"USER SCORE : {db[key].score}")
                    print(f"BEST WORD : {db[key].best_word}")
                    print(f"BEST SCORE : {db[key].best_score}")
                    print()
                print()
    else:
        print("Invalid parameters.\n'play' to start a new round\n'list' to get a list of every game you ever played")

if __name__ == "__main__":
    main()
