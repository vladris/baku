from datetime import datetime
import os
import re
from baku import consts


UNICODE_ALNUM_PTN = re.compile(r'[\W_]+', re.U)


def name_from_title(title):
    word_sep = consts.SLUG_WORD_SEPARATOR

    return UNICODE_ALNUM_PTN.sub(word_sep, title).lower().strip(word_sep)


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def parse_date(str_date):
    return datetime.strptime(str_date, '%Y/%m/%d')


def split_date(date):
    return f'{date.year:04}', f'{date.month:02}', f'{date.day:02}'


def path_from_date(date):
    return ensure_path(os.path.join(*split_date(date)))


def open_utf8(file, mode):
    return open(file, mode, encoding='utf8')
