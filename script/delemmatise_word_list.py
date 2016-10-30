'''
Given JSON files nouns.json and verbs.json with simple, flat lists of words,
create appropriate variants.
'''
import spacy

import re
import simplejson as json


print '>> loading JSON definitions'
nouns = {
    'plain': [unicode(word) for word in json.load(open('nouns.json'))],
    'plural': {}
}

print '>> loading NLP corpus'
nlp = spacy.load('en')
all_strings = [string for string in nlp.vocab.strings]


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


def tag_filter_pos(tags, start, end):
    return [word for word, pos in tags
            if pos.startswith(start) and pos.endswith(end)]


# nouns: create plurals
print '>> finding plurals'
num_matches = []

for noun in nouns['plain']:
    prefix_length = 3
    if len(noun) > prefix_length:
        prefix = noun[:-prefix_length]
    else:
        prefix = noun

    matches = all_strings
    matches = filter_match(matches, r'^' + prefix)
    matches = filter_similar_length(matches, noun)
    matches = filter_not_match(matches, '\.$')
    matches = filter_not_match(matches, '-[a-z]$')
    matches += [noun]

    lemma_matches = filter_lemma_match(matches, noun)

    tagged = tag(lemma_matches)

    final = tag_filter_pos(tagged, start='N', end='S')

    # if there are multiple choices, choose the most popular
    if len(final) > 1:
        final = filter_highest_ranking(final)

    # try a simple modification
    if len(final) != 1:
        simple_plural = noun + 's'
        if simple_plural in matches:
            final = [simple_plural]

    # still no matches? use original word
    if not final:
        final = [noun]

    print '\t' + noun + ': ' + str(final)
    nouns['plural'][noun] = final[0]


with open('nouns.extra.json', 'w') as output_file:
    json.dump(nouns, output_file)
