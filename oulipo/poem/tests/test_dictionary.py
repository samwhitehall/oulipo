#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from poem.models.dictionaries import AlphabeticalDictionary, load


class TestDictionary(unittest.TestCase):
    def setUp(self):
        words = [
            'Elephant',
            'Dog',
            'Cat',
            'Butterfly',
            'Aardvark',
        ]
        self.dictionary = AlphabeticalDictionary(words)

    def test_contains_words(self):
        self.assertTrue('Aardvark' in self.dictionary)

    def test_ordering(self):
        self.assertEqual(self.dictionary[0], 'Aardvark')
        self.assertEqual(self.dictionary[1], 'Butterfly')
        self.assertEqual(self.dictionary[2], 'Cat')
        self.assertEqual(self.dictionary[3], 'Dog')
        self.assertEqual(self.dictionary[4], 'Elephant')

    def test_get_offset_edge_case(self):
        self.assertEqual(self.dictionary[-2], 'Aardvark')  # first item
        self.assertEqual(self.dictionary[50], 'Elephant')  # last item

    def test_find(self):
        self.assertEqual(self.dictionary.find('Aaaaaa'), -0.5)
        self.assertEqual(self.dictionary.find('Cat'), 2)
        self.assertEqual(self.dictionary.find('Catamaran'), 2.5)
        self.assertEqual(self.dictionary.find('Caterpillar'), 2.5)
        self.assertEqual(self.dictionary.find('Dog'), 3)
        self.assertEqual(self.dictionary.find('Xylophone'), 4.5)

    def test_advance_by_zero(self):
        word = self.dictionary.advance('Butterfly', 0)
        self.assertEqual(word, 'Butterfly')

    def test_advance_in_range(self):
        plus_one = self.dictionary.advance('Butterfly', 1)
        self.assertEqual(plus_one, 'Cat')

        minus_one = self.dictionary.advance('Butterfly', -1)
        self.assertEqual(minus_one, 'Aardvark')

    def test_advance_out_range(self):
        over = self.dictionary.advance('Dog', 3)
        self.assertEqual(over, 'Elephant')

        under = self.dictionary.advance('Butterfly', -4)
        self.assertEqual(under, 'Aardvark')

    def test_advance_from_outside_range(self):
        before = self.dictionary.advance('Aaaa', -1)
        self.assertEqual(before, 'Aaaa')

        minus_one = self.dictionary.advance('Zzzz', 1)
        self.assertEqual(minus_one, 'Zzzz')

    def test_advance_missing_word(self):
        word = self.dictionary.advance('Chimpanzee', 1)
        self.assertEqual(word, 'Dog')

        word = self.dictionary.advance('Chimpanzee', -1)
        self.assertEqual(word, 'Cat')

        word = self.dictionary.advance('Chimpanzee', 2)
        self.assertEqual(word, 'Elephant')

        word = self.dictionary.advance('Chimpanzee', -2)
        self.assertEqual(word, 'Butterfly')

    def test_advance_unicode_word(self):
        word = self.dictionary.advance(u'çat', 1)
        self.assertEqual(word, 'Dog')


class TestWordCase(unittest.TestCase):
    def test_non_lowercase_word_in_dictionary(self):
        words = [
            'apple',
            'Bulgaria',
            'coal',
        ]
        dictionary = AlphabeticalDictionary(words)

        self.assertTrue('bulgaria' in dictionary)
        self.assertEqual(dictionary.find('bulgaria'), 1)
        self.assertEqual(dictionary.advance('apple', 1), 'Bulgaria')

    def test_non_lowercase_word_given(self):
        words = [
            'apple',
            'blossom',
            'coal',
        ]
        dictionary = AlphabeticalDictionary(words)

        self.assertTrue('Blossom' in dictionary)
        self.assertEqual(dictionary.find('Blossom'), 1)
        self.assertEqual(dictionary.advance('Apple', 1), 'blossom')


class TestDictionaryLoader(unittest.TestCase):
    def test_loader(self):
        expected = [
            'Aardvark',
            'Butterfly',
            'Cat',
            'Dog',
            'Elephant',
        ]

        dictionary = load('test', full=True)

        self.assertEqual(dictionary.word_list, expected)
