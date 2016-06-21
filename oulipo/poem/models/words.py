# TODO: add docstrings
import re


from poem.common import PARTS_OF_SPEECH
from poem.models.dictionaries import load
from poem.tasks import process_lines

dictionaries = {
    'noun': load('nouns'),
    'verb': load('verbs'),
}


class Options(object):
    def __init__(self, advance_by__noun=0, advance_by__verb=0):
        self.advance_by__noun = advance_by__noun
        self.advance_by__verb = advance_by__verb

        self.advance_by = {
            'noun': self.advance_by__noun,
            'verb': self.advance_by__verb,
        }

    def __repr__(self):
        return repr(self.advance_by)


class Token(object):
    def __init__(self, category, original_word=None, content=None):
        self.category = category

        if content is not None:
            self.content = content

        if original_word is not None:
            self.original_word = original_word

        if category in PARTS_OF_SPEECH and original_word is None:
            self.original_word = self.content

    def __repr__(self):
        template = '({self.category})'
        if hasattr(self, 'original_word'):
            template += ' {self.original_word} -> {self.content}'

        return template.format(self=self)

    def replace_word(self, new_word):
        if self.category not in PARTS_OF_SPEECH:
            raise Exception('Cannot replace word. Token is not PoS')

        original = self.original_word.strip()
        self.content = self.original_word.replace(original, new_word)


class Poem(object):
    def __init__(self, raw_text, options, tokens=None):
        self.raw_text = raw_text
        self.options = Options(**options)

        if tokens is not None:
            self.tokens = [Token(**token) for token in tokens]
        else:
            self.tokens = tokenize(raw_text)

        advance_and_replace(self, dictionaries)


def tokenize(raw_text):
    raw_text = unicode(raw_text)
    lines = re.split(r'(\n)', raw_text)

    processed = process_lines.delay(lines).get()
    tokens = [Token(category, content) for category, content in processed]

    return tokens


def advance_and_replace(poem_model, dictionaries):
    # TODO: return new object rather than mutating
    advance_by = poem_model.options.advance_by
    if not advance_by:
        return

    tokens = poem_model.tokens

    to_replace = [token for token in tokens if token.category in advance_by]

    for token in to_replace:
        dictionary = dictionaries[token.category]
        offset = advance_by[token.category]
        word = token.original_word.strip()

        new_word = dictionary.advance(word, offset)
        token.replace_word(new_word)
