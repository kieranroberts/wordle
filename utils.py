from functools import reduce
from collections import Counter


def find_indices(*, word, w):
    return [i for i, x in enumerate(word) if x in w]


def letter_counts(*, guess, pattern):
    # wc = Counter(guess)
    # for w, v in wc.items():
    lc = list()
    m = pattern.count("n")
    for w in set(guess):
        I = find_indices(word=guess, w=w)
        I_c = [i for i in range(len(guess)) if i not in I]
        sub_pattern = [pattern[i] for i in I]
        sub_pattern_c = [pattern[i] for i in I_c]
        n = len(find_indices(word=sub_pattern, w="cp"))
        n0 = len(find_indices(word=sub_pattern_c, w="r"))
        if "n" not in sub_pattern and "r" not in sub_pattern:
            n = n + m + n0
        # n = len(I)
        # n0 = len(find_indices(sub_pattern, "r"))
        lc.append((w, n))

    return lc


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


def filter_words(*, words: list, letter: str, idx: int, present, pos) -> list:
    if present and pos:
        return list(filter(lambda x: letter == x[idx], words))
    elif present and not (pos):
        return list(filter(lambda x: letter in x and letter != x[idx], words))
    elif not (present) and not (pos):
        return list(filter(lambda x: letter not in x, words))


def find_most_likely_words(*, words: list) -> dict:
    word_freq = word_frequencies(words=words)
    k_max = ""
    v_max = 0
    for k, v in word_freq.items():
        if v > v_max:
            v_max = v
            k_max = k
            # print(k_max)
    return k_max


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
    return
