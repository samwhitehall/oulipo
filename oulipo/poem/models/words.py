# TODO: add docstrings
import re
from collections import OrderedDict

from celery.exceptions import TimeoutError
from django.conf import settings

from poem.common import PARTS_OF_SPEECH, TAGS, ServerException, OFFSETS
from poem.models.dictionaries import load
from poem.tasks import process_lines


DICTIONARIES = {
    'noun': load('nouns', full=True),
    'verb': load('verbs', full=True),
}

TRANSFORM_TO = {
    'NNS': load('nns'),
    'VBD': load('vbd'),
    'VBG': load('vbg'),
    'VBN': load('vbn'),
    'VBZ': load('vbz'),
}


class Token(object):
    def __init__(self, category, original_word=None, tag=None):
        self.category = category

        if original_word is not None:
            self.original_word = original_word

        if tag in TAGS:
            self.tag = tag

    def __repr__(self):
        template = '({self.category})'
        if hasattr(self, 'original_word'):
            template += ' "{self.original_word}"'

        return template.format(self=self)

    @property
    def offsets(self):
        if self.category not in PARTS_OF_SPEECH:
            return {}

        offset_words = OrderedDict()
        original = self.original_word.strip()

        for offset in OFFSETS:
            dictionary = DICTIONARIES[self.category]
            # TODO: improve this by only doing one call
            word = dictionary.advance(original, offset)

            if hasattr(self, 'tag'):
                word = TRANSFORM_TO[self.tag].get(word, word)

            word = self.original_word.replace(original, word)
            offset_words[offset] = word

        return offset_words


class Poem(object):
    def __init__(self, title, raw_text, tokens=None):
        self.title = title
        self.raw_text = raw_text
        self.tokens = tokenize(raw_text)


def tokenize(raw_text):
    raw_text = unicode(raw_text)
    lines = re.split(r'(\n)', raw_text)

    try:
        processed = process_lines\
                .delay(lines)\
                .get(timeout=settings.CELERY_TIMEOUT)
    except TimeoutError:
        raise ServerException('Request timed out.')

    tokens = [Token(category, original_word=original_word, tag=tag)
              for original_word, category, tag in processed]

    return tokens
