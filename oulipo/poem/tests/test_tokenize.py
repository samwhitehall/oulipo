from collections import namedtuple
import unittest

from celery import current_app
from django.conf import settings
from mock import patch
import spacy.parts_of_speech as pos

from poem.tasks import process_lines


Token = namedtuple('Token', ['string', 'pos'])


def test_tagger(line, tag=None, parse=None):
    nouns = {'world', 'cat'}

    tokens = []
    for word in line.split(' '):
        token = Token(word, pos.NOUN if word in nouns else pos.PART)
        tokens.append(token)

    return tokens


class TestTokenization(unittest.TestCase):
    def setUp(self):
        settings.CELERY_ALWAYS_EAGER = True
        current_app.conf.CELERY_ALWAYS_EAGER = True

    def test_tokenize(self):
        with patch.dict('poem.tasks._nlp', {'en': test_tagger}):
            lines = ['hello world and cat']
            expected = [
                ('other', 'hello'),
                ('noun', 'world'),
                ('other', 'and'),
                ('noun', 'cat'),
            ]
            processed = process_lines.delay(lines).get()

            self.assertEqual(processed, expected)
