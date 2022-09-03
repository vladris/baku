from datetime import datetime
import os
import re
from baku import consts


UNICODE_ALNUM_PTN = re.compile(r'[\W_]+', re.U)


def name_from_title(title):
    try:
        word_sep = consts.SLUG_WORD_SEPARATOR
    except Exception:
        word_sep = '_'

    return UNICODE_ALNUM_PTN.sub(word_sep, title).lower().strip(word_sep)


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def parse_date(str):
    return datetime.strptime(str, '%Y/%m/%d')


def split_date(date):
    return '%04d' % date.year, '%02d' % date.month, '%02d' % date.day


def path_from_date(date):
    return ensure_path(os.path.join(*split_date(date)))
