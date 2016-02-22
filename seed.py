#!/usr/bin/env python

import logging
from itertools import islice

import click
from db.seed import seed_db_with_comments


@click.command()
@click.argument('comments_filename')
@click.option('-l', '--limit', default=-1)
def run_seed(
    comments_filename,
    limit,
):
    with open(comments_filename) as comments_file:
        if limit != -1:
            comments_file = islice(comments_file, int(limit))
        for num_comments, num_markov_entries in seed_db_with_comments(comments_file):
            if not num_comments % 25 == 0:
                continue
            logging.info('Seeded {} comments and {} markov entries'.format(num_comments, num_markov_entries))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_seed()
