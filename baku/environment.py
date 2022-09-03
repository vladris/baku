from struct import pack
from baku import consts, utils
import os
import shutil


def init_folder(package_path, folder, files):
    utils.ensure_path(folder)
    for f in files:
        shutil.copy(
            os.path.join(package_path, 'templates', f),
            folder)


def initialize():
    package_path = os.path.abspath(os.path.dirname(__file__))

    init_folder(package_path, 'templates', [consts.POST_TEMAPLTE, consts.ROOT_TEMPLATE])
    init_folder(package_path, 'static', ['style.css', 'pygments.css', 'icon.ico'])
    init_folder(package_path, '.', [consts.CONFIG])

    print('All set! Don\'t forget to update blog.conf.')


def is_blog():
    return os.path.exists(consts.CONFIG)


def load_config():
    config = {}
    for line in open(consts.CONFIG, 'r').readlines():
        line = line.strip()
        if not line:
            continue

        key, value = line.split('=', 1)
        config[key.strip()] = value.strip()

    return config
