import os.path
import simplejson as json


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

    def advance(self, word, n):
        if n == 0:
            return word

        if word not in self:
            # TODO: include logic for if the word is not in the dictionary
            return word

        index = self.index[word]
        return self[index + n]


def load(name):
    if not name.endswith('.json'):
        name = name + '.json'

    path = os.path.join(settings.BASE_DIR, 'poem/data', name)
    words = json.load(open(path))

    return AlphabeticalDictionary(words)
