import unittest

from celery import current_app
from django.conf import settings
from mock import patch
from rest_framework.test import APIRequestFactory

from poem.models.dictionaries import load
from poem.tests.test_tokenize import test_tagger
from poem.views import PoemViewSet


DICTIONARY = load('test', full=True)


class TestApiEndpoint(unittest.TestCase):
    def setUp(self):
        settings.CELERY_ALWAYS_EAGER = True
        current_app.conf.CELERY_ALWAYS_EAGER = True

    @patch.dict('poem.tasks._nlp', {'en': test_tagger})
    @patch.dict('poem.models.words.DICTIONARIES', {'noun': DICTIONARY})
    def test_initial_post(self):
        api = APIRequestFactory()

        text = 'hello Cat i am a Dog'
        options = {
            'advance_by__noun': 1,
        }

        request = api.post('/poems/', {
            'title': 'my brilliant poem',
            'raw_text': text,
            'options': options,
        }, format='json')

        view = PoemViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['raw_text'], text)
        self.assertEqual(response.data['options'], {
            'advance_by__noun': 1,
            'advance_by__verb': 0,  # not specified => default to 0
        })

        expected_new_text = 'hello Dog i am a Elephant'.replace(' ', '')
        new_text = ''.join(token['content']
                           for token in response.data['tokens'])
        self.assertEqual(new_text, expected_new_text)

        self.assertEqual(response.data['tokens'][1]['original_word'], 'Cat')
        self.assertEqual(response.data['tokens'][-1]['original_word'], 'Dog')
