import unittest

from rest_framework.test import APIRequestFactory

from poem.serializers import (
    PoemModelSerializer,
    TokenSerializer,
)


class TestApiValidation(unittest.TestCase):
    def test_missing_fields(self):
        serializer = PoemModelSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'raw_text': [u'This field is required.'],
            'title': [u'This field is required.']
        })


    def test_field_length(self):
        poem = {
            'title': '',
            'raw_text': 'foo' * 9999,
            'options': {},
        }
        serializer = PoemModelSerializer(data=poem)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'raw_text': ['Ensure this field has no more than 2000 characters.'],
        })
