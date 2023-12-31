#!/usr/bin/env python3

import click
import requests
import re
from bs4 import BeautifulSoup

def get_html_of(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)

    return resp.content.decode()

def count_occurrences_in(word_list, min_length):
    word_count = {}

    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    return word_count

def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)

def get_top_words_from(all_words, min_length):
    occurrences = count_occurrences_in(all_words, min_length)
    sorted_occurrences = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)
    return [word for word, count in sorted_occurrences if len(word) >= min_length]

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=9, help='Minimum word length (default: 9).')
def main(url, length):
    the_words = get_all_words_from(url)
    top_words = get_top_words_from(the_words, length)

    # Check if there are at least 3 words in the top list
    if len(top_words) >= 3:
        print(f'The 3rd most frequent word with a minimum length of {length} is: {top_words[2]}')
    else:
        print('There are fewer than 3 words in the top list.')

if __name__ == '__main__':
    main()
