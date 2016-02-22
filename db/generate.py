import random
from . import markov_dict, comments, SYMS_START, PREFIX_LEN, SYMS_END


def _choose_next_word(prefix):
    record = markov_dict.find_one({'prefix': prefix})
    suffixes = record['suffixes']
    return random.choice(suffixes)


def _comment_exists(comment):
    if comment is None:
        return True
    return comments.find({'comment': comment}).count() != 0


def generate_comment():
    comment = None
    while _comment_exists(comment):
        words = SYMS_START[:]
        while words[-1] != SYMS_END[-1]:
            prefix = ' '.join(words[-PREFIX_LEN:])
            suffix = _choose_next_word(prefix)
            words.append(suffix)
        comment = ' '.join(words[PREFIX_LEN:-PREFIX_LEN])
    return comment
