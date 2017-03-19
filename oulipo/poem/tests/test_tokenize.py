from collections import namedtuple
import unittest

from celery import current_app
from django.conf import settings
from mock import patch
from spacy.parts_of_speech import NOUN, PART

from poem.tasks import process_lines


Token = namedtuple('Token', ['string', 'pos', 'tag_', 'is_stop'])


def test_tagger(line, tag=None, parse=None):
    nouns = {'World', 'Cat', 'Cats', 'Dog', 'Macaque'}
    stopwords = {'and'}

    tokens = []
    for word in line.split(' '):
        pos = NOUN if word in nouns else PART
        tag = 'NNS' if word.endswith('s') else None
        stop = word in stopwords

        token = Token(word + ' ', pos, tag, stop)
        tokens.append(token)

    return tokens


class TestTokenization(unittest.TestCase):
    def setUp(self):
        settings.CELERY_ALWAYS_EAGER = True
        current_app.conf.CELERY_ALWAYS_EAGER = True

    def test_tokenize(self):
        with patch.dict('poem.tasks._nlp', {'en': test_tagger}):
            lines = ['hello World and Cats']
            expected = [
                ('hello ', 'other', None),
                ('World ', 'noun', None),
                ('and ', 'other', None),
                ('Cats ', 'noun', 'NNS'),
            ]
            processed = process_lines.delay(lines).get()

            self.assertEqual(processed, expected)
