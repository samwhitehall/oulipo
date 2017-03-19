PARTS_OF_SPEECH = [
    'noun',
    'verb',
]

CATEGORIES = PARTS_OF_SPEECH + [
    'punctuation',
    'new_line',
    'other',
]

TAGS = [
    'NNS',
    'VBD',
    'VBG',
    'VBN',
    'VBZ',
]

OFFSETS = range(-10, 11)


class ServerException(Exception):
    pass
