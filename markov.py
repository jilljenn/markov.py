from lea import Lea
from collections import Counter


sentences = ['je mange des cerises', 'je mange des bananes', 'je conduis des camions']
next_one = {}
for sentence in sentences:
    words = sentence.split()
    n = len(words)
    for i in range(n - 1):
        if words[i] not in next_one:
            next_one[words[i]] = Counter()
        next_one[words[i]][words[i + 1]] += 1
states = {}
for word in next_one:
    states[word] = Lea.fromValFreqsDict(next_one[word])
# print(states)

word = 'je'
for _ in range(3):
    print(word)
    word = states[word].random()
print(word)
