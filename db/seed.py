from . import comments, markov_dict, SYMS_START, SYMS_END, PREFIX_LEN


def seed_db_with_comments(lines_iter):
    num_comments = 0
    num_markov_entries = 0
    for line in lines_iter:
        comment = line.strip()
        if comments.find_one({'comment': comment}) is not None:
            continue
        comments.insert_one({
            'comment': comment
        })
        num_comments += 1
        words = SYMS_START + line.split() + SYMS_END
        for i in range(len(words) - PREFIX_LEN):
            prefix = ' '.join(words[i:i + PREFIX_LEN])
            suffix = words[i + PREFIX_LEN]
            markov_dict.find_one_and_update(
                {'prefix': prefix},
                {'$push': {'suffixes': suffix}},
                upsert=True,
            )
            num_markov_entries += 1
    return num_comments, num_markov_entries
