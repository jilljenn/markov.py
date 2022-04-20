from collections import Counter, defaultdict
import argparse
import random
from lea import Lea


BOS_TOKEN = -2
EOS_TOKEN = -1


def markov(corpus, n_seq=1, start=None, length=42):
    # Counting occurrences
    next_one = defaultdict(Counter)
    next_one[EOS_TOKEN][EOS_TOKEN] = 1  # Last state is absorbing
    for sentence in corpus:
        words = sentence.split()
        nb_words = len(words)
        next_one[BOS_TOKEN][words[0]] += 1
        for i in range(nb_words - 1):
            next_one[words[i]][words[i + 1]] += 1
        if nb_words:
            final_word = words[nb_words - 1]
            next_one[final_word][EOS_TOKEN] += 1

    # Initializing states
    states = {}
    for state in next_one:
        states[state] = Lea.fromValFreqsDict(next_one[state])

    # Outputting visited states
    for _ in range(n_seq):
        state = start if start is not None else BOS_TOKEN
        seq = [state]
        while len(seq) < length and state != EOS_TOKEN:
            state = states[state].random()
            seq.append(state)
        print(' '.join(filter(lambda x: x not in {BOS_TOKEN, EOS_TOKEN}, seq)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates tokens.')
    parser.add_argument('filename', type=str, nargs='?', default='text',
                        help='Try files in demo/ e.g. "demo/text.txt"')
    parser.add_argument('--n', type=int, nargs='?', default=1,
                        help='How many sequences should be printed')
    parser.add_argument('--l', type=int, nargs='?', default=42,
                        help='Length of these sequences')
    args = parser.parse_args()

    with open(args.filename) as f:
        corpus = f.read().splitlines()

    start = None
    length = args.l
    if args.filename == 'demo/music.txt':  # Generating music note by note
        # This corpus contains "Für Elise" from Beethoven, and some Bach
        start = 'e'
        length = 20
    elif args.filename == 'demo/words.txt':  # Generating words from letters
        start = 'a'
        length = 12

    markov(corpus, args.n, start, length)
