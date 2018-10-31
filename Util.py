import sys


def progress(filename, now, total):
    bar_len = 60
    filled_len = int(round(bar_len * now / float(total)))

    percent = round(100.0 * now / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)

    end = '\n' if percent == 100 else '\r'

    sys.stdout.write('%s: [%s] %s%s%s' % (filename, bar, percent, '%', end))
    sys.stdout.flush()
