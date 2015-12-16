def make_syms(prefix_len):
    syms_start = ['__start{}__'.format(i) for i in range(prefix_len)]
    syms_end = ['__end{}__'.format(i) for i in range(prefix_len)]
    return syms_start, syms_end
