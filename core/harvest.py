import json
from itertools import islice

import click
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict


def make_syms(prefix_len):
    syms_start = ['__start{}__'.format(i) for i in range(prefix_len)]
    syms_end = ['__end{}__'.format(i) for i in range(prefix_len)]
    return syms_start, syms_end


OUT_DIR = 'out'


@click.command()
@click.argument('root_url')
@click.option('--limit', 'comments_limit', default=1000)
@click.option('--prefix-len', '-p', default=3)
@click.option('-o', 'out_filename', default='comments.json')
def scrape_comments_at_url(
    root_url,
    comments_limit,
    prefix_len,
    out_filename,
):
    comments = list(islice(scrape_root_url(root_url), comments_limit))
    markov_dict = build_markov_dict(comments, prefix_len)
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    os.chdir(OUT_DIR)
    with open(out_filename, 'w') as f:
        obj = {
            'root_url': root_url,
            'prefix_len': prefix_len,
            'num_comments': len(comments),
            'comments': comments,
            'prefix_dict': markov_dict
        }
        json.dump(obj, f, indent=1)
        print("Wrote {} comments to {}".format(len(comments), out_filename))


def markov_dict_add_line(line, markov_dict, prefix_len, syms_start, syms_end):
    words = syms_start + line + syms_end
    for i in range(len(words) - prefix_len):
        prefix = ' '.join(words[i:i + prefix_len])
        suffix = words[i + prefix_len]
        markov_dict[prefix].append(suffix)


def build_markov_dict(lines, prefix_len=3):
    markov_dict = defaultdict(list)
    syms = make_syms(prefix_len)
    for line in lines:
        words = line.split()
        markov_dict_add_line(words, markov_dict, prefix_len, *syms)
    return markov_dict


def scrape_root_url(root_url):
    visited = set()
    queue = [(root_url, 'Root')]
    while True:
        url, title = queue.pop()
        visited.add(url)
        raw_html = requests.get(url).text
        root = BeautifulSoup(raw_html, 'lxml')
        comments = list(harvest_comments(root))
        print('Harvested {} comments from {} "{}"'.format(len(comments), url, title))
        yield from comments
        for link_span_div in root.find_all('span', {'class': 'title'}):
            anchor = link_span_div.find('a')
            href = anchor.attrs['href']
            if 'view_video.php' not in href:
                continue
            next_url = 'http://www.pornhub.com' + href
            if next_url in visited:
                continue
            next_title = anchor.attrs['title']
            queue.append((next_url, next_title))


def harvest_comments(root):
    for comment_div in root.find_all('div', {'class': 'commentMessage'}):
        comment_content = next(comment_div.children)
        comment_text = ' '.join(str(comment_content).split())
        yield comment_text + '\n'


if __name__ == '__main__':
    scrape_comments_at_url()
