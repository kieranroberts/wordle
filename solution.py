import os
from itertools import combinations
from collections import Counter
from argparse import ArgumentParser
from random import sample
from functools import reduce


def filter_words(*, words: list, letter: str, idx: int, present, pos) -> list:
    if present and pos:
        return list(filter(lambda x: letter == x[idx], words))
    elif present and not (pos):
        return list(filter(lambda x: letter in x and letter != x[idx], words))
    elif not (present) and not (pos):
        return list(filter(lambda x: letter not in x, words))


def letter_freq(*, words: list) -> dict:
    freq = Counter("".join(words))
    total_count = sum(freq.values())
    for k, v in freq.items():
        freq[k] = v / total_count
    return freq


def word_likelihood(*, letter_freq: dict, word: str) -> float:
    letter_probs = [letter_freq[x] for x in word]
    prob = reduce(lambda x, y: x * y, letter_probs, 1)
    return prob


def word_frequencies(*, words: list) -> dict:
    freq = letter_freq(words=words)
    word_freq = dict()
    for w in words:
        word_prob = word_likelihood(letter_freq=freq, word=w)
        word_freq[w] = word_prob
    return word_freq


def find_most_likely_words(*, words: list) -> dict:
    word_freq = word_frequencies(words=words)
    k_max = ""
    v_max = 0
    for k, v in word_freq.items():
        if v > v_max:
            v_max = v
            k_max = k
            print(k_max)
    return v_max


# Step 1:
# 1. Guess AROSE
word = [
    ("a", False, False),
    ("r", False, False),
    ("o", False, False),
    ("s", False, False),
    ("e", False, False),
]


def find_candidates(*, words: list, comb: int) -> list:
    best = list()
    while len(best) < 500:
        for x in combinations(words, comb):
            n = len(set("".join(x)))
            if n == 5 * comb:
                best.append(x)
                print(x)
    return best


def find_candidates2(*, words: list, base: list, comb: int) -> list:
    best = list()
    for w in words:
        x = tuple(base) + (w,)
        n = len(set("".join(x)))
        if n == comb * 5:
            best.append(x)
    return best


def main():
    with open(input_file, "r") as f:
        words = [w.rstrip() for w in f.readlines()]

    n_max = 0
    best_max = list()
    for i in range(10):
        print(f"Iteration {i+1}..")
        words0 = sample(words, 50)
        n, best = find_candidates(words=words, comb=comb_size)
        if n > n_max:
            best_max = best
        elif n == n_max:
            best_max.extend(best)

    with open(output_file, "r") as f:
        f.write(f"Maximum letter coverage: {n}\n\n")
        for w in best_max:
            f.write(", ".join(w) + "\n")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script to generate monthly census/panel volume reports."
    )
    parser.add_argument("-i", "--input", help="Input file with words", required=True)
    parser.add_argument(
        "-n", "--num", help="Size of word tuples", required=True, type=int
    )
    parser.add_argument("-o", "--output", help="Output file", required=True)

    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    comb_size = args.num

    main()
