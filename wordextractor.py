import click
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_html_of(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content.decode()

def count_occurrences_in(word_list, min_length):
    word_count = {}

    for word in word_list:
        if len(word) < min_length:
            continue
        word_count[word] = word_count.get(word, 0) + 1

    return word_count

def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)

def get_top_words_from(all_words, min_length, top_count):
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)[:top_count]

def generate_password_mutations(word):
    mutations = [
        word, 
        word.capitalize(), 
        word.lower(), 
        word.upper(),
        f"{word}2019",
        f"{word}1!",
        f"{word}2!",
        f"{word}3!",
        f"{word}01",
        f"{word}123",
        f"Summer{word}2021!",
        # Add more mutations as needed
    ]
    return mutations

def crawl_page(url, depth, min_length, top_count, output_file):
    if depth <= 0:
        return

    the_words = get_all_words_from(url)
    top_words = get_top_words_from(the_words, min_length, top_count)

    with open(output_file, 'a') as output:
        for word, count in top_words:
            output.write(f'{word}: {count}\n')
            
            # Add password mutations to the output
            mutations = generate_password_mutations(word)
            for mutation in mutations:
                output.write(f'{mutation}\n')

        # Get all URLs from the page and crawl them
        soup = BeautifulSoup(get_html_of(url), 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            next_url = urljoin(url, link['href'])
            crawl_page(next_url, depth-1, min_length, top_count, output_file)

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).')
@click.option('--top', '-t', default=10, help='Number of top words to display (default: 10).')
@click.option('--output', '-o', help='Output file to print to instead of the console.')
@click.option('--depth', '-d', default=1, help='Crawl depth of the script (default: 1).')
def main(url, length, top, output, depth):
    if length >= 10:
        print("Error: Minimum length must be less than 10.")
        return

    if output:
        # Clear existing content if output file is specified
        with open(output, 'w'):
            pass

    crawl_page(url, depth, length, top, output or '/dev/stdout')

if __name__ == '__main__':
    main()
