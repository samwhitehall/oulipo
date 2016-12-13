# TODO: add docstrings
import itertools
import re

from poem.common import PARTS_OF_SPEECH, TAGS
from poem.models.dictionaries import load
from poem.tasks import process_lines

from django.db import models
from django.utils.text import slugify


DICTIONARIES = {
    'noun': load('nouns', full=True),
    'verb': load('verbs', full=True),
}

TRANSFORM_TO = {
    'NNS': load('nns'),
    'VBD': load('vbd'),
    'VBG': load('vbg'),
    'VBN': load('vbn'),
    'VBZ': load('vbz'),
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
    def __init__(self, category, original_word=None, content=None, tag=None):
        self.category = category

        if content is not None:
            self.content = content

        if original_word is not None:
            self.original_word = original_word

        if category in PARTS_OF_SPEECH and original_word is None:
            self.original_word = self.content

        if tag in TAGS and tag is not None:
            self.tag = tag

    def __repr__(self):
        template = '({self.category})'
        if hasattr(self, 'original_word'):
            template += ' "{self.original_word}" -> "{self.content}"'

        return template.format(self=self)

    def replace_word(self, new_word):
        if self.category not in PARTS_OF_SPEECH:
            raise Exception('Cannot replace word. Token is not PoS')

        original = self.original_word.strip()
        self.content = self.original_word.replace(original, new_word)


class Poem(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    raw_text = models.TextField()
    slug = models.SlugField(primary_key=True)
    options = Options()
    tokens = []

    @classmethod
    def create(cls, title, raw_text, options, tokens=None, slug=''):
        options = Options(**options)

        if tokens:
            tokens = [Token(**token) for token in tokens]
        else:
            tokens = tokenize(raw_text)

        poem = Poem.objects.filter(slug=slug, raw_text=raw_text, title=title)
        if poem.exists():
            poem = poem[0]
        else:
            slug = Poem.generate_slug(title, raw_text)
            poem = cls(title=title, raw_text=raw_text, slug=slug)

        poem.options = options
        poem.tokens = tokens

        advance_and_replace(poem)
        return poem

    @classmethod
    def generate_slug(self, title, raw_text, max_length=24):
        title_slug = slugify(title)
        text_slug = slugify(raw_text)

        if len(title_slug) > max_length:
            slug = title_slug
        else:
            slug = (title_slug + '-' + text_slug)

        slug = slug[:max_length].rstrip('-')

        # if the slug already exists, randomise until we find a unique slug
        new_slug = slug
        for count in itertools.count(1):
            if not Poem.objects.filter(slug=new_slug).exists():
                break
            new_slug = slug + '-' + str(count)

        return new_slug


def tokenize(raw_text):
    raw_text = unicode(raw_text)
    lines = re.split(r'(\n)', raw_text)

    processed = process_lines.delay(lines).get()
    tokens = [Token(category, content=content, tag=tag)
              for content, category, tag in processed]

    return tokens


def advance_and_replace(poem_model):
    # TODO: return new object rather than mutating
    advance_by = poem_model.options.advance_by
    if not advance_by:
        return

    tokens = poem_model.tokens

    to_replace = [token for token in tokens if token.category in advance_by]

    for token in to_replace:
        dictionary = DICTIONARIES[token.category]
        offset = advance_by[token.category]
        word = token.original_word.strip()

        new_word = dictionary.advance(word, offset)

        if hasattr(token, 'tag'):
            new_word = TRANSFORM_TO[token.tag].get(new_word, new_word)

        token.replace_word(new_word)
