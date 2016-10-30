'''
Parse 5000 most frequent words into noun/verb dictionaries using HTML file
downloaded from wordfrequency.info. Each of these is already lemmatised.
'''
from collections import defaultdict
import simplejson as json

from bs4 import BeautifulSoup

# from http://ucrel.lancs.ac.uk/claws7tags.html
part_of_speech_codes = {
    'a': 'article',
    'c': 'conjunction',
    'd': 'determiner',
    'e': 'existentialthere',
    'i': 'preposition',
    'j': 'adjective',
    'm': 'number',
    'n': 'noun',
    'p': 'pronoun',
    'r': 'adverb',
    't': 'infinitive marker',
    'u': 'interjection',
    'v': 'verb',
    'x': 'negative',
}

# load and parse html table
with open('script/wordfrequency.info.html') as html_file:
    html = html_file.read()

parsed = BeautifulSoup(html, 'lxml')
tables = parsed.find_all('table')
main_table = tables[3]
rows = main_table.find_all('tr')[2:]

assert len(rows) == 5000

words = defaultdict(list)

for idx, row in enumerate(rows):
    rank, word, part_of_speech, _, _ = row.find_all('td')

    rank = int(rank.text)
    word = word.text.strip()
    part_of_speech = part_of_speech.text

    assert idx == rank - 1
    words[part_of_speech].append(word)

for part_of_speech, pos_words in words.items():
    words[part_of_speech] = set(pos_words)


# print statistics
def print_stats():
    for code, pos_words in words.items():
        print '{} ({}): {}'.format(
            part_of_speech_codes[code], code, len(pos_words))


print_stats()
print '---'


# remove words that may be offensive
blacklisted = set(json.load(open('script/blacklist.json')))
for pos_words in words.values():
    pos_words -= blacklisted

print 'Remove Blacklisted Words'
print_stats()
print '---'

# export files
outputs = ['n', 'v']
for output_type in outputs:
    file_name = part_of_speech_codes[output_type] + 's.json'
    with open(file_name, 'w') as output_file:
        json.dump(sorted(words[output_type]), output_file)

        print '-> written to ' + file_name
