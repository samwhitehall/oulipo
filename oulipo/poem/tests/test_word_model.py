import unittest
from mock import patch

from poem.models.dictionaries import load
from poem.models.words import (
    Poem,
    Token,
    advance_and_replace
)

DICTIONARY = load('test', full=True)


class TestTokenModel(unittest.TestCase):
    def test_category_pos(self):
        token = Token('noun', content='elephant')

        self.assertEqual(token.category, 'noun')
        self.assertEqual(token.content, 'elephant')
        self.assertEqual(token.original_word, 'elephant')

    def test_category_other(self):
        token = Token('punctuation', content='$')

        self.assertEqual(token.category, 'punctuation')
        self.assertEqual(token.content, '$')
        self.assertFalse(hasattr(token, 'original_word'))

    def test_replace_word_pos(self):
        token = Token('noun', content='elephant')
        token.replace_word('fox')

        self.assertEqual(token.category, 'noun')
        self.assertEqual(token.content, 'fox')
        self.assertEqual(token.original_word, 'elephant')

    def test_replace_word_preserves_spacing(self):
        token = Token('noun', content='  elephant   ')
        token.replace_word('fox')

        self.assertEqual(token.content, '  fox   ')

    def test_replace_word_non_pos(self):
        token = Token('punctuation', content='$')

        with self.assertRaises(Exception):
            token.replace_word('blah')


class TestPoemModel(unittest.TestCase):
    @patch('poem.models.words.tokenize')
    @patch('poem.models.words.advance_and_replace')
    def test_initial_not_yet_tokenised(self, mock_advance, mock_tokenize):
        title = 'My Wonderful Poem'
        raw_text = 'Hello world.'
        options = {}

        poem = Poem(title, raw_text, options)

        mock_tokenize.assert_called_with(raw_text)
        mock_advance.assert_called_with(poem)

    @patch('poem.models.words.advance_and_replace')
    def test_subsequent_already_tokenised(self, mock_advance):
        title = 'My Wonderful Poem'
        raw_text = 'Hello world.'
        options = {}
        tokens = [
            {'category': 'other', 'content': 'Hello'},
            {'category': 'noun', 'content': 'world'},
            {'category': 'punctuation', 'content': '.'},
        ]

        poem = Poem(title, raw_text, options, tokens)

        mock_advance.assert_called_with(poem)

    @patch('poem.models.words.tokenize')
    def test_slug_generation(self, mock_tokenize):
        long_title = Poem(
            title='This is a poem with a long title', raw_text='', options={})
        self.assertEqual(
            long_title.generate_slug(), 'this-is-a-poem-with-a-lo')

        short_title = Poem(
            title='Short title', raw_text='This is a poem with a short title',
            options={})
        self.assertEqual(
            short_title.generate_slug(), 'short-title-this-is-a-po')


class TestAdvanceReplace(unittest.TestCase):
    @patch('poem.models.words.advance_and_replace')
    @patch.dict('poem.models.words.DICTIONARIES', {'noun': DICTIONARY})
    def test_advance_replace(self, mock_advance):
        title = 'My Wonderful Poem'
        raw_text = 'Cat and Dog'
        tokens = [
            {'category': 'noun', 'content': 'Cat'},
            {'category': 'other', 'content': ' and '},
            {'category': 'noun', 'content': 'Dog'},
        ]
        options = {'advance_by__noun': 1}

        # don't do advance_and_replace on poem creation (mocked out)
        poem = Poem(title, raw_text, options, tokens)

        advance_and_replace(poem)

        self.assertEqual(poem.tokens[0].content, 'Dog')
        self.assertEqual(poem.tokens[1].content, ' and ')
        self.assertEqual(poem.tokens[2].content, 'Elephant')
