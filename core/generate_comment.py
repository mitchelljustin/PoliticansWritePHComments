import random


def make_syms(prefix_len):
    syms_start = ['__start{}__'.format(i) for i in range(prefix_len)]
    syms_end = ['__end{}__'.format(i) for i in range(prefix_len)]
    return syms_start, syms_end


def generate_pornhub_comment(markov_dict, prefix_len, blacklist=None):
    if blacklist is None:
        blacklist = {}
    syms_start, syms_end = make_syms(prefix_len)
    words = syms_start
    while words[-1] != syms_end[-1]:
        prefix = ' '.join(words[-prefix_len:])
        choices = markov_dict[prefix]
        suffix = random.choice(choices)
        while suffix in syms_end and random.random() < 0.75 and set(choices) != set(syms_end):
            suffix = random.choice(choices)
        words.append(suffix)
    sentence_str = ' '.join(words[prefix_len:-prefix_len]) + '\n'
    if sentence_str in blacklist:
        return generate_pornhub_comment(markov_dict, prefix_len, blacklist)
    return sentence_str
