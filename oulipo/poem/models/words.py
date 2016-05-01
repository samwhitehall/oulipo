# TODO: add docstrings
import re


from poem.common import PARTS_OF_SPEECH
from poem.models.dictionaries import load
from poem.tasks import process_lines

dictionary = load('nouns')


class Options(object):
    def __init__(self, advance_by):
        self.advance_by = advance_by

    def __repr__(self):
        return repr(self.advance_by)


class Token(object):
    def __init__(self, category, content=None):
        self.category = category

        if content is not None:
            self.content = content

        if category in PARTS_OF_SPEECH:
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
        self.options = options

        if tokens is not None:
            self.tokens = tokens
        else:
            self.tokens = tokenize(raw_text)

        advance_and_replace(self, dictionary)


def tokenize(raw_text):
    raw_text = unicode(raw_text)
    lines = re.split(r'(\n)', raw_text)

    processed = process_lines.delay(lines).get()
    tokens = [Token(category, content) for category, content in processed]

    return tokens


def advance_and_replace(poem_model, dictionaries):
    # TODO: return new object rather than mutating
    tokens = poem_model.tokens
    advance_by = poem_model.options.advance_by

    to_replace = [token for token in tokens if token.category in advance_by]

    for token in to_replace:
        dictionary = dictionaries[token.category]
        offset = advance_by[token.category]
        word = token.original_word.strip()

        new_word = dictionary.advance(word, offset)
        token.replace_word(new_word)
