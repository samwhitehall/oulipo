import re

import spacy.en
import spacy.parts_of_speech as pos

from poem.common import PARTS_OF_SPEECH


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


class Poem(object):
    def __init__(self, raw_text, options, tokens=None):
        self.raw_text = raw_text
        self.options = options

        if tokens is not None:
            self.tokens = tokens
        else:
            self.tokens = tokenize(raw_text)


def tokenize(raw_text):
    parts_of_speech = {
        pos.NOUN: 'noun',
        pos.VERB: 'verb',
        pos.PUNCT: 'punctuation',
    }
    nlp = spacy.en.English()

    raw_text = unicode(raw_text)
    lines = re.split(r'(\n)', raw_text)
    processed_lines = [nlp(line, tag=True, parse=False) for line in lines]

    tokens = []
    for line in processed_lines:
        for token in line:
            content = token.string
            category = parts_of_speech.get(token.pos, 'other')

            if '\n' in token.string:
                category = 'new_line'

            tokens.append(Token(category, content))

    return tokens
