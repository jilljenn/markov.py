from collections import Counter, defaultdict
import argparse
import random
from lea import Lea


def markov(corpus, n_seq=1, start=None, length=42):
    # Counting occurrences
    next_one = defaultdict(Counter)
    for sentence in corpus:
        words = sentence.split()
        nb_words = len(words)
        for i in range(nb_words - 1):
            next_one[words[i]][words[i + 1]] += 1
        if nb_words:
            final_word = words[nb_words - 1]
            next_one[final_word][-1] += 1
            next_one[-1][-1] += 1  # Last state is absorbing

    # Initializing states
    states = {}
    for word in next_one:
        states[word] = Lea.fromValFreqsDict(next_one[word])

    # Outputting visited states
    for _ in range(n_seq):
        word = start if start is not None else random.choice(list(states.keys()))
        for _ in range(length):
            if word == -1:
                break
            print(word, end=' ')
            word = states[word].random()
        if word != -1:
            print(word, end='')
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates tokens.')
    parser.add_argument('filename', type=str, nargs='?', default='text',
                        help='For a demo, try files in demo/ or "demo:word"')
    parser.add_argument('--n', type=int, nargs='?', default=1,
                        help='How many sequences should be printed')
    parser.add_argument('--l', type=int, nargs='?', default=42,
                        help='Length of these sequences')
    args = parser.parse_args()

    with open(args.filename) as f:
        corpus = f.read().splitlines()

    start = None
    length = args.l
    if args.filename == 'demo/text.txt':  # Generating sentences word by word
        start = 'je'
        length = 3
    elif args.filename == 'demo/music.txt':  # Generating music note by note
        # This corpus contains "Für Elise" from Beethoven, and some Bach
        start = 'e'
        length = 20
    elif args.filename == 'demo/words.txt':  # Generating words from letters
        start = 'a'
        length = 12

    markov(corpus, args.n, start, length)
