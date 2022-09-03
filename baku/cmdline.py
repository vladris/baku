import argparse
import shutil
import baku
from baku import build, document, utils
from datetime import datetime
import os


def initialize():
    utils.ensure_path('templates')
    utils.ensure_path('static')

    for f in ['post.html', 'index.html']:
        shutil.copy(utils.get_template(f), os.path.join('templates', f))
    
    for f in ['style.css', 'icon.ico']:
        shutil.copy(utils.get_template(f), os.path.join('static', f))


def create_post(title, date):
    path = utils.path_from_date(date)

    if os.path.exists(title):
        new_post = document.move(title, path)
        print(f'Draft moved to post {new_post}')
    else:
        new_post = document.create_document(title, path)
        print(f'New post created as {new_post.path}')


def create_draft(title):
    if os.path.exists(title):
        new_draft = document.move(title, 'drafts')
        print(f'File moved to draft {new_draft}')
    else:
        new_draft = document.create_draft(title)
        print(f'New draft created as {new_draft.path}')


def main(argv=None):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-i', '--init', action='store_true',
        help='initialize a new blog')
    group.add_argument('-b', '--build', action='store_true', help='build blog')
    group.add_argument(
        '-p', '--post', nargs=1,
        help='create a new post with the title POST (if a file named POST '
        'exists, it is moved to a new post instead)')
    group.add_argument(
        '-d', '--draft', nargs=1,
        help='creates a new draft with the title DRAFT (if a file named DRAFT '
        'exists, it is moved to a new draft instead)')
    group.add_argument(
        '-v', '--version', action='store_true',
        help='display version information')
    parser.add_argument(
        '--date', nargs=1,
        help='optionally specify a date as "YYYY/mm/dd" for the post, '
        'useful when migrating blogs; can only be used together with '
        '-p/--post')

    command = parser.parse_args(argv)

    post_date = None
    if command.date:
        # --date only works with --post
        if not command.post:
            print('Can only use --date with -p/--post.')
            return -1

        try:
            post_date = datetime.strptime(command.date[0], '%Y/%m/%d')
        except Exception:
            print('Invalid post date: format should be YYYY/mm/dd')
            return -1
    else:
        post_date = datetime.today()


    if command.init:
        initialize()
    elif command.build:
        build.build()
    elif command.post:
        create_post(command.post[0], post_date)
    elif command.draft:
        create_draft(command.draft[0])
    elif command.version:
        print(f'Baku version {baku.__version__} ')
    else:
        parser.print_help()

    return 0
