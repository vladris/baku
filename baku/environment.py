import os
import shutil
from typing import Dict, List
from baku import consts, utils


def init_folder(package_path: str, folder: str, files: List[str]) -> None:
    utils.ensure_path(folder)
    for f in files:
        shutil.copy(
            os.path.join(package_path, 'templates', f),
            folder)


def initialize() -> None:
    package_path = os.path.abspath(os.path.dirname(__file__))

    init_folder(package_path, 'templates', consts.TEMPLATES)
    init_folder(package_path, 'static', consts.STATICS)
    init_folder(package_path, '.', [consts.CONFIG])

    print('All set! Don\'t forget to update blog.conf.')


def is_blog() -> bool:
    return os.path.exists(consts.CONFIG)


def load_config(file: str = consts.CONFIG) -> Dict[str, str]:
    config = {}
    with utils.open_utf8(file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            key, value = line.split('=', 1)
            config[key.strip()] = value.strip()

    return config
