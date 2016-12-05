import math
import os.path
import simplejson as json
import string

from bisect import bisect

from django.conf import settings
from unidecode import unidecode


class AlphabeticalDictionary:
    def __init__(self, words):
        normalised = [word.lower() for word in words]
        assert len(words) == len(set(normalised)), \
            'Word list contains duplicates'

        self.word_list = sorted(words, key=string.lower)
        self.word_list_normalised = sorted(normalised)
        self.index = {
            word: index for index, word in enumerate(self.word_list)}

        # also include lower-case variants of words in index
        for word in words:
            if word.lower() not in self.index:
                self.index[word.lower()] = self.index[word]

    def __contains__(self, word):
        return word in self.index or word.lower() in self.index

    def __getitem__(self, index):
        if index < 0:
            return self.word_list[0]

        if index > len(self.word_list) - 1:
            return self.word_list[-1]

        return self.word_list[index]

    def find(self, word):
        word = unidecode(unicode(word))

        if word in self.index:
            return self.index[word]

        if word.lower() in self.index:
            return self.index[word.lower()]

        insert_index = bisect(self.word_list_normalised, word.lower())
        return insert_index - 0.5

    def advance(self, word, n):
        if n == 0:
            return word

        index = self.find(word)

        # if the initial word is outside of the bounds of the dictionary,
        # and we are advancing further outside
        if index < 0 and n < 0:
            return word

        max_index = len(self.word_list) - 1
        if index > max_index and n > 0:
            return word

        # if we have a fractional index, advance up and down to nearest
        # integer
        if n < 0:
            new_index = int(math.ceil(index + n))
        else:
            new_index = int(math.floor(index + n))

        return self[new_index]


def load(name, full=False):
    if not name.endswith('.json'):
        name = name + '.json'

    path = os.path.join(settings.BASE_DIR, '../poem/data', name)
    words = json.load(open(path))

    dictionary = words
    if full:
        dictionary = AlphabeticalDictionary(words)

    return dictionary
