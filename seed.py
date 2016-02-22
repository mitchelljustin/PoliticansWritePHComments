#!/usr/bin/env python

import logging

import click
from db.seed import seed_db_with_comments


@click.command()
@click.argument('comments_filename')
def run_seed(
    comments_filename
):
    with open(comments_filename) as comments_file:
        num_comments, num_markov_entries = seed_db_with_comments(comments_file)
        logging.info('Seeded {} comments and {} markov entries'.format(num_comments, num_markov_entries))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_seed()
