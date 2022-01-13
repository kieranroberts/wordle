from collections import Counter
from argparse import ArgumentParser
import numpy as np
from utils import *

with open("sgb-words.txt") as f:
    words = [word.rstrip() for word in f.readlines()]


def next_guess(*, words: list, prev_word: str, pattern: str) -> str:
    words0 = words
    # do the letter count filter here
    lc = letter_counts(guess=prev_word, pattern=pattern)
    for w, c in lc:
        words0 = list(filter(lambda x: x.count(w) <= c, words0))
    for idx, w in enumerate(prev_word):
        if pattern[idx] == "p":
            present = True
            pos = False
        elif pattern[idx] == "n":
            present = False
            pos = False
        elif pattern[idx] == "c":
            present = True
            pos = True
        else:
            continue
        words0 = filter_words(words=words0, letter=w, idx=idx, present=present, pos=pos)

    guess = find_most_likely_words(words=words0)
    return guess, words0


def calculate_pattern(*, answer: str, guess: str) -> str:
    pattern = str()
    lc = Counter(answer)
    for idx, w in enumerate(guess):
        if w not in answer:
            pattern += "n"
        elif w in answer and answer[idx] != w and lc[w] >= 1:
            pattern += "p"
            lc[w] = lc[w] - 1
        elif answer[idx] == w and lc[w] >= 1:
            pattern += "c"
            lc[w] = lc[w] - 1
        elif lc[w] <= 0:
            pattern += "r"
    return pattern


def enter_pattern(*, guess, answer):
    if answer:
        pattern = calculate_pattern(answer=answer, guess=guess)
    else:
        pattern = input("Enter Wordle matching output: ")
        pattern = pattern.lower()
        while len(list(filter(lambda x: x in "npcr", pattern))) != 5:
            pattern = input(
                "Must be 5-letter string of N (not present),P (present but not correct position) and C (present and correct position): "
            )

    return pattern


def solve_word(*, answer, first_guess, print_guesses=True):
    count = 1
    pattern = "nnnnn"
    words0 = words
    if first_guess:
        guess = first_guess
    else:
        guess = input("Enter your first guess: ")
        while guess not in words:
            guess = input("Enter a valid 5-letter word: ")

    while pattern != "ccccc" and count < 6:
        pattern = enter_pattern(guess=guess, answer=answer)
        if pattern == "ccccc":
            break
        guess, words0 = next_guess(words=words0, prev_word=guess, pattern=pattern)
        if print_guesses:
            print(f"Your next guess is {guess}")
        count += 1

    if count <= 6:
        pattern = enter_pattern(guess=guess, answer=answer)
    if pattern != "ccccc":
        if print_guesses:
            print("You did not guess within 6 attempts. Fail")
            return [0, answer]
        else:
            return [0, answer]
    else:
        if print_guesses:
            print(f"You guessed {guess} correctly in {count} attempts.")
            return count
        else:
            return count


def solve_all_words(*, answers, first_guess, print_output=True, write_fails=False):
    counts = list()
    fails = list()
    with open(answers) as f:
        all_words = [word.rstrip() for word in f.readlines()]
    for answer in all_words:
        count = solve_word(answer=answer, first_guess=first_guess, print_guesses=False)
        if isinstance(count, list):
            fails.append(count[1])
            count = count[0]
        counts.append(count)
    if write_fails:
        with open(f"words/{first_guess}.txt", "w") as f:
            f.write("\n".join(fails))
    avg_guesses = np.mean(list(filter(lambda x: x > 0, counts)))
    freq = Counter(counts)
    num_guesses = 0
    for k, v in freq.items():
        if k == 0:
            num_guesses += 7 * v
        else:
            num_guesses += k * v
    if print_output == True:
        print(
            f"Total number of guesses: {num_guesses}\nAverage number of guesses: {avg_guesses}\nNumber of failed guesses: {freq[0]}"
        )
        return first_guess, num_guesses, freq[0], avg_guesses
    else:
        return first_guess, num_guesses, freq[0], avg_guesses


def modify_dict_upto_key(my_dict, key):
    remove_keys = list()
    for k, v in my_dict.items():
        if k != "least":
            remove_keys.append(k)
        elif k == "least":
            remove_keys.append(k)
            break
    for k in remove_keys:
        my_dict.pop(k)
    return my_dict


def best_first_guess(*, answers, first_guesses, print_output=True):
    least_guesses = ([], np.inf)
    least_fails = ([], np.inf)
    least_mean = ([], np.inf)
    with open(first_guesses) as f:
        all_guesses = [word.rstrip() for word in f.readlines()]

    all_guesses = word_frequencies(words=all_guesses)
    all_guesses = {
        k: v
        for k, v in sorted(all_guesses.items(), key=lambda item: item[1], reverse=True)
    }
    # all_guesses = modify_dict_upto_key(all_guesses, """)

    for guess, val in all_guesses.items():
        g, num_guesses, num_fails, avg_guesses = solve_all_words(
            answers=answers,
            first_guess=guess,
            print_output=False,
        )
        if num_guesses < least_guesses[1]:
            least_guesses = ([g], num_guesses)
            print(f"{least_guesses[0]} has least number of guesses: {least_guesses[1]}")
        elif num_guesses == least_guesses[1]:
            least_guesses[0].append(g)
            print(f"{least_guesses[0]} has least number of guesses: {least_guesses[1]}")

        if num_fails < least_fails[1]:
            least_fails = ([g], num_fails)
            print(f"{least_fails[0]} has least number of fails: {least_fails[1]}")
        elif num_fails == least_fails[1]:
            least_fails[0].append(g)
            print(f"{least_fails[0]} has least number of fails: {least_fails[1]}")

        if avg_guesses < least_mean[1]:
            least_mean = ([g], avg_guesses)
            print(f"{least_mean[0]} has least average guesses: {least_mean[1]:.4f}")
        elif avg_guesses == least_mean[1]:
            least_mean[0].append(g)
            print(f"{least_mean[0]} has least number of fails: {least_mean[1]:.4f}")

    if print_output:
        print(f"{least_guesses[0]} has least number of guesses: {least_guesses[1]}")
        print(f"{least_fails[0]} has least number of fails: {least_fails[1]}")
        print(f"{least_mean[0]} has least number of fails: {least_mean[1]:.4f}")
        return least_guesses, least_fails
    else:
        return least_guesses, least_fails


def main(answer, answers, first_guess, first_guesses):
    if not (answers):
        solve_word(answer=answer, first_guess=first_guess)
    elif answers and first_guess:
        solve_all_words(answers=answers, first_guess=first_guess)
    elif answers and first_guesses:
        best_first_guess(answers=answers, first_guesses=first_guesses)


if __name__ == "__main__":
    parser = ArgumentParser(description="Wordle solver.")
    ans = parser.add_mutually_exclusive_group(required=False)
    gss = parser.add_mutually_exclusive_group(required=False)
    ans.add_argument("-a", "--answer", help="Option to let computer play by itself")
    ans.add_argument("-A", "--answers", help="List of words separated by newlines")
    gss.add_argument("-g", "--guess", help="First guess")
    gss.add_argument("-G", "--guesses", help="List of guesses separated by newlines")

    args = parser.parse_args()
    answer = args.answer
    answers = args.answers
    first_guess = args.guess
    first_guesses = args.guesses

    main(answer, answers, first_guess, first_guesses)
