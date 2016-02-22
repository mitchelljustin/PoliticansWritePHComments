from itertools import islice

import click
import os
import requests
from bs4 import BeautifulSoup

OUT_DIR = 'out'


@click.command()
@click.argument('root_url')
@click.option('--limit', 'comments_limit', default=10000)
@click.option('-o', 'out_filename', default='comments.json')
def scrape_comments_at_url(
    root_url,
    comments_limit,
    out_filename,
):
    comments = list(islice(scrape_root_url(root_url), comments_limit))
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    os.chdir(OUT_DIR)
    with open(out_filename, 'w') as f:
        f.writelines(comments)
    print("Wrote {} comments to {}".format(len(comments), out_filename))


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
