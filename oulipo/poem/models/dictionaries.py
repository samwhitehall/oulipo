import math
import os.path
import simplejson as json

from bisect import bisect


from django.conf import settings


class AlphabeticalDictionary:
    def __init__(self, words):
        self.word_list = sorted(words)
        self.index = {
            word: index for index, word in enumerate(self.word_list)}

    def __contains__(self, word):
        return word in self.index

    def __getitem__(self, index):
        if index < 0:
            return self.word_list[0]

        if index > len(self.word_list):
            return self.word_list[-1]

        return self.word_list[index]

    def find(self, word):
        if word in self.index:
            return self.index[word]

        insert_index = bisect(self.word_list, word)
        return insert_index - 0.5

    def advance(self, word, n):
        if n == 0:
            return word

        index = self.find(word)

        # if we have a fractional index, advance up and down to nearest
        # integer
        if n < 0:
            new_index = int(math.ceil(index + n))
        else:
            new_index = int(math.floor(index + n))

        return self[new_index]


def load(name):
    if not name.endswith('.json'):
        name = name + '.json'

    path = os.path.join(settings.BASE_DIR, '../poem/data', name)
    words = json.load(open(path))

    return AlphabeticalDictionary(words)
