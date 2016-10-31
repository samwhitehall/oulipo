'''
De-Lemmatise Word List

Given JSON files nouns.json and verbs.json with simple, flat lists of words,
create appropriate variants.

The relevant PoS transformations are:
    - NNS: noun (plural)
    - VBD: verb (past tense)
    - VBG: verb (present participle)
    - VBN: verb (past participle)
    - VBZ: verb (3rd person singular present)

(https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)

Usage:
    delemmatise_word_list.py [--only=<tokens>] [--test]

Options:
    --only=<tokens>     Comma separated PoS token types to calculate,
                        can also use N/V for all noun/verb types respectively
    --test              Try with 50 words to get an idea of results.
'''
import re
from collections import OrderedDict

from docopt import docopt
import simplejson as json
import spacy


TEST_MODE = None
nlp = None
all_strings = []
nouns = []
verbs = []


def filter_match(word_list, re_string):
    regex = re.compile(re_string)
    return filter(regex.search, word_list)


def filter_not_match(word_list, re_string):
    regex = re.compile(re_string)
    return filter(lambda word: not regex.search(word), word_list)


def filter_similar_length(word_list, comparison):
    return [word for word in word_list
            if abs(len(word) - len(comparison)) <= 3]


def filter_lemma_match(word_list, comparison):
    return [word for word in word_list
            if nlp(word)[0].lemma_ == comparison.lower()]


def filter_most_similar(word_list, comparison):
    comparison_token = nlp(comparison)[0]

    highest_similarity_measure = 0
    highest_similarity_word = None

    for word in word_list:
        similarity = nlp(word)[0].similarity(comparison_token)
        if similarity > highest_similarity_measure:
            highest_similarity_measure = similarity
            highest_similarity_word = word

    return [highest_similarity_word]


def tag(words):
    return [(word, nlp(word)[0].tag_) for word in words]


def filter_highest_ranking(word_list):
    most_popular_rank = float('inf')
    most_popular_word = None

    for word in word_list:
        rank = nlp(word)[0].rank
        if rank < most_popular_rank:
            most_popular_rank = rank
            most_popular_word = word

    return [most_popular_word]


def filter_very_rare_words(word_list):
    threshold = 160000
    return [word for word in word_list
            if nlp(word)[0].rank < threshold]


def tag_filter_pos(tags, valid_tags):
    return [word for word, pos in tags if pos in valid_tags]


def create_initial_guesses_by_prefix(word):
    prefix_length = 3
    if len(word) > prefix_length:
        prefix = word[:-prefix_length]
    else:
        prefix = word

    matches = all_strings
    matches = filter_match(matches, r'^' + prefix)

    return matches


def apply_broad_filters(matches, word):
    matches = filter_similar_length(matches, word)
    matches = filter_not_match(matches, '\.$')
    matches = filter_not_match(matches, '-[a-z]$')
    matches += [word]

    return matches


def make_plural(noun):
    return [
        noun + 's',
    ]


def make_present_tense(verb):
    return [
        verb + 'ing',
        verb[:-1] + 'ing',
        verb + verb[:-1] + 'ing',
    ]


def make_past_tense(verb):
    return [
        verb + 'd',
        verb + 'ed',
    ]


def make_third_person_present(verb):
    return [
        verb + 's',
    ]


add_regular_forms_functions = {
    'NNS': make_plural,
    'VBD': make_past_tense,
    'VBG': make_present_tense,
    'VBN': make_past_tense,
    'VBZ': make_third_person_present,
}

suffixes = {
    'NNS': 's',
    'VBG': 'ing',
    'VBZ': 's',
}


def calculate_word_type(part_of_speech):
    '''Find the correct form of word for the given pos tag.'''

    add_regular_forms = add_regular_forms_functions[part_of_speech]
    suffix = suffixes.get(part_of_speech, '')

    result = OrderedDict()

    word_lists = {
        'N': nouns,
        'V': verbs,
    }
    word_list = word_lists[part_of_speech[0]]

    if TEST_MODE:
        print '>> test mode enabled (only using first 50 words)'
        word_list = word_list[:50]

    print '>> calculating forms for ' + part_of_speech
    for word in word_list:
        broad_matches = create_initial_guesses_by_prefix(word)
        broad_matches = apply_broad_filters(broad_matches, word)

        matches = filter_lemma_match(broad_matches, word)
        matches = tag_filter_pos(tag(matches), [part_of_speech])

        # filter by suffix
        matches = [match for match in matches if match.endswith(suffix)]

        # add regular forms to see
        if len(word) >= 3:
            for modified in add_regular_forms(word):
                if modified not in matches and modified in all_strings:
                    matches.append(modified)

        # filter very rare forms
        matches = filter_very_rare_words(matches)

        # still no matches? use original word
        if not matches:
            matches = [word]

        # if there are multiple choices, choose the most popular
        if len(matches) > 1:
            matches = filter_highest_ranking(matches)

        print '\t' + word + ': ' + str(matches)
        result[word] = (matches[0])

    return result


if __name__ == '__main__':
    print '>> parse arguments'
    arg = docopt(__doc__)
    to_execute = []

    TEST_MODE = arg['--test']

    all_pos = add_regular_forms_functions.keys()
    if arg['--only'] is None:
        to_execute = all_pos
    if arg['--only'] == 'N':
        to_execute = [pos for pos in all_pos if pos.startswith('N')]
    if arg['--only'] == 'V':
        to_execute = [pos for pos in all_pos if pos.startswith('V')]
    if arg['--only'] in all_pos:
        to_execute = [arg['--only']]
    if ',' in str(arg['--only']):
        to_execute = arg['--only'].split(',')

    assert to_execute, 'No function to execute'

    print '>> load JSON definitions'
    nouns = [unicode(word) for word in json.load(open('nouns.json'))]
    verbs = [unicode(word) for word in json.load(open('verbs.json'))]

    print '>> load NLP corpus'
    nlp = spacy.load('en')
    all_strings = [string for string in nlp.vocab.strings]

    for pos in to_execute:
        result = calculate_word_type(pos)

        file_name = pos.lower() + '.json'
        print '>> write to ' + file_name
        with open(file_name, 'w') as output_file:
            json.dump(result, output_file)
