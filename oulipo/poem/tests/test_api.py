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

        text = 'I am' + '\n' + 'a Macaque'

        request = api.post('/poems/', {
            'title': 'My Brilliant Poem',
            'raw_text': text,
        }, format='json')

        view = PoemViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['raw_text'], text)

        # one big expected value
        self.assertEqual(response.data['tokens'], [
            {
                'original_word': 'I ',
                'category': 'other',
                'offsets': {}
            },
            {
                'original_word': 'am ',
                'category': 'other',
                'offsets': {}
            },
            {
                'original_word': '\n ',
                'category': 'new_line',
                'offsets': {}
            },
            {
                'original_word': 'a ',
                'category': 'other',
                'offsets': {}
            },
            {
                'original_word': 'Macaque ',
                'category': 'noun',
                'offsets': {
                    '-10': 'Dog ',
                    '-9': 'Elephant ',
                    '-8': 'Frog ',
                    '-7': 'Gorilla ',
                    '-6': 'Hummingbird ',
                    '-5': 'Ibis ',
                    '-4': 'Jackal ',
                    '-3': 'Kingfisher ',
                    '-2': 'Lemur ',
                    '-1': 'Macacque ',
                    '0': 'Macaque ',
                    '1': 'Narwhal ',
                    '2': 'Octopus ',
                    '3': 'Penguin ',
                    '4': 'Quokka ',
                    '5': 'Rabbit ',
                    '6': 'Spider ',
                    '7': 'Tiger ',
                    '8': 'Unicorn ',
                    '9': 'Unicorn ',
                    '10': 'Unicorn '
                 }
            }
        ])

    def test_validation(self):
        api = APIRequestFactory()
        view = PoemViewSet.as_view({'post': 'create'})

        request = api.post('/poems/', {}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors'], {
            'raw_text': [u'This field is required.'],
            'title': [u'This field is required.']
        })

    def test_server_error(self):
        api = APIRequestFactory()
        view = PoemViewSet.as_view({'post': 'create'})

        request = api.post('/poems/', {
            'title': '',
            'raw_text': 'hello world',
        }, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data['errors'], ['Corpus not initialised.'])
