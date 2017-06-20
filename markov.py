from lea import Lea
from collections import Counter, defaultdict
import argparse
import os


WORD_LIST_URL = 'http://www.pallier.org/extra/liste.de.mots.francais.frgut.txt'


def markov(corpus, start, length):
    # Counting occurrences
    next_one = defaultdict(Counter)
    for sentence in corpus:
        words = sentence.split()
        nb_words = len(words)
        for i in range(nb_words - 1):
            next_one[words[i]][words[i + 1]] += 1

    # Initializing states
    states = {}
    for word in next_one:
        states[word] = Lea.fromValFreqsDict(next_one[word])

    # Outputting visited states
    word = start
    for _ in range(length):
        print(word, end=' ')
        word = states[word].random()
    print(word)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Displays a demo.')
    parser.add_argument('demo_type', type=str, nargs='?', default='text',
                        help='a type of demo: "text", "music" or "word"')
    args = parser.parse_args()

    if args.demo_type == 'text':
        # Generating sentences word by word
        corpus = ['je mange des cerises',
                  'je mange des bananes',
                  'je conduis des camions']
        start = 'je'
        length = 3
    elif args.demo_type == 'music':
        # Generating music note by note
        corpus = ['e d# e d# e b d c a',  # Lettre à Élise de Beethoven
                  'C E g c e g c e C E g c e g c e C D a d f a d f']  # Bach
        start = 'e'
        length = 20
    elif args.demo_type == 'word':
        # Generating words letter by letter
        if not os.path.isfile('liste.de.mots.francais.frgut.txt'):
            print('Downloading {}…'.format(WORD_LIST_URL))
            os.system('wget {}'.format(WORD_LIST_URL))
        corpus = [' '.join(list(word)) for word in
                  open(os.path.basename(WORD_LIST_URL)).read().splitlines()]
        start = 'a'
        length = 12

    markov(corpus, start, length)
