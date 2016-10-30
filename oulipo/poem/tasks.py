import spacy.en
import spacy.parts_of_speech as pos

from celery import shared_task
from celery.signals import worker_init

_nlp = {}


# load nlp corpus on worker initialisation
def _load_nlp_corpus(**kwargs):
    if not _nlp:
        _nlp['en'] = spacy.load('en')

worker_init.connect(_load_nlp_corpus)


@shared_task
def process_lines(lines):
    if not _nlp:
        raise Exception('corpus not initialised')

    parts_of_speech = {
        pos.NOUN: 'noun',
        pos.VERB: 'verb',
        pos.PUNCT: 'punctuation',
    }

    # TODO: pass exceptions properly
    lines = [_nlp['en'](line, tag=True, parse=False) for line in lines]

    # TODO: better name for processed
    # TODO: do this processing back in model? i.e. serialize tokens
    processed = []
    for line in lines:
        for token in line:
            content = token.string
            category = parts_of_speech.get(token.pos, 'other')

            if '\n' in token.string:
                category = 'new_line'

            processed.append((category, content))

    return processed
