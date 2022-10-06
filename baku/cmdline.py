import argparse
from datetime import datetime
import baku
from baku import build, document, environment, upgrade, utils


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
    group.add_argument(
        '-u', '--upgrade', action='store_true',
        help='upgrade blog templates')
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
            post_date = utils.parse_date(command.date[0])
        except ValueError:
            print('Invalid post date: format should be YYYY/mm/dd')
            return -1
    else:
        post_date = datetime.today()


    if command.init:
        environment.initialize()
        return 0

    # All commands except initialize need to run from blog root
    if not environment.is_blog():
        print('Run baku from blog root or initialize a blog here using --init')
        return -1

    if command.build:
        build.build()
    elif command.post:
        document.create_or_move_post(command.post[0], post_date)
    elif command.draft:
        document.create_or_move_draft(command.draft[0])
    elif command.upgrade:
        upgrade.upgrade()
    elif command.version:
        print(f'Baku version {baku.__version__} ')
    else:
        parser.print_help()

    return 0
