import unittest
from mock import patch

from poem.models.dictionaries import load as load_dictionary
from poem.models.words import (
    Poem,
    Options,
    Token,
    advance_and_replace,
    dictionaries,
)


class TestTokenModel(unittest.TestCase):
    def test_category_pos(self):
        token = Token('noun', 'elephant')

        self.assertEqual(token.category, 'noun')
        self.assertEqual(token.content, 'elephant')
        self.assertEqual(token.original_word, 'elephant')

    def test_category_other(self):
        token = Token('punctuation', '$')

        self.assertEqual(token.category, 'punctuation')
        self.assertEqual(token.content, '$')
        self.assertFalse(hasattr(token, 'original_word'))

    def test_replace_word_pos(self):
        token = Token('noun', 'elephant')
        token.replace_word('fox')

        self.assertEqual(token.category, 'noun')
        self.assertEqual(token.content, 'fox')
        self.assertEqual(token.original_word, 'elephant')

    def test_replace_word_non_pos(self):
        token = Token('punctuation', '$')

        with self.assertRaises(Exception):
            token.replace_word('blah')


class TestPoemModel(unittest.TestCase):
    @patch('poem.models.words.tokenize')
    @patch('poem.models.words.advance_and_replace')
    def test_initial_not_yet_tokenised(self, mock_advance, mock_tokenize):
        raw_text = 'Hello world.'
        options = {}

        poem = Poem(raw_text, options)

        mock_tokenize.assert_called_with(raw_text)
        mock_advance.assert_called_with(poem, dictionaries)

    @patch('poem.models.words.advance_and_replace')
    def test_subsequent_already_tokenised(self, mock_advance):
        raw_text = 'Hello world.'
        options = {}
        tokens = [
            Token('other', 'Hello'),
            Token('noun', 'world'),
            Token('punctutaion', '.'),
        ]

        poem = Poem(raw_text, options, tokens)

        mock_advance.assert_called_with(poem, dictionaries)


class TestAdvanceReplace(unittest.TestCase):
    @patch('poem.models.words.advance_and_replace')
    def test_advance_replace(self, mock_advance):
        raw_text = 'Cat and Dog'
        tokens = [
            Token('noun', 'Cat'),
            Token('other', ' and '),
            Token('noun', 'Dog'),
        ]
        options = Options(advance_by={'noun': 1})

        # don't do advance_and_replace on poem creation (mocked out)
        poem = Poem(raw_text, options, tokens)

        test_dictionaries = {
            'noun': load_dictionary('test'),
        }

        advance_and_replace(poem, test_dictionaries)

        self.assertEqual(poem.tokens[0].content, 'Dog')
        self.assertEqual(poem.tokens[1].content, ' and ')
        self.assertEqual(poem.tokens[2].content, 'Elephant')
