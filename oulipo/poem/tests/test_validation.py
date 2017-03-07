import unittest

from rest_framework.test import APIRequestFactory

from poem.serializers import (
    OptionsSerializer, 
    PoemModelSerializer, 
    TokenSerializer,
)


class TestApiValidation(unittest.TestCase):
    def test_missing_fields(self):
        serializer = PoemModelSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'raw_text': [u'This field is required.'], 
            'options': [u'This field is required.'], 
            'title': [u'This field is required.']
        })

    def test_invalid_options(self):
        options = {
            'advance_by__noun': 'a',
            'advance_by__verb': 100,
        }
        serializer = OptionsSerializer(data=options)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'advance_by__noun': [u'A valid integer is required.'], 
            'advance_by__verb': 
                [u'Ensure this value is less than or equal to 10.'], 
        })

    def test_token_consistency(self):
        no_original = {
            'category': 'noun',
            'content': 'foo',
        }
        serializer = TokenSerializer(data=no_original)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'non_field_errors': ['Missing original_word.'],
        })

        newline = {
            'category': 'new_line',
            'content': 'foo',
        }
        serializer = TokenSerializer(data=newline)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'non_field_errors': ['Inconsistent newline.'],
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
