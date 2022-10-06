import html
import os
from typing import Callable, Dict, Tuple
from baku import templating, utils


class Post:
    # pylint: disable=too-many-instance-attributes
    # These are all needed for template rendering and addressing this would
    # force us to do more awkward things.
    def __init__(self, doc: str):
        self.doc = doc

        # Timestamp
        _, year, month, day, _ = doc.split(os.path.sep)
        self.date = utils.parse_date(f'{year}/{month}/{day}').astimezone()

        # Load content
        with utils.open_utf8(doc, 'r') as f:
            self.text = f.read()

        self.title = html.unescape(self.text.split('\n', 1)[0].strip(' #'))
        self.body = None

        # Relative path and link
        self.rel_path = (os.path.splitext(doc)[0] + '.html').replace(
            os.path.pathsep, '/')
        self.href = '../../../' + self.rel_path[2:]

        self.prev, self.next = None, None


    # Get destination directory and file
    def get_dest(self) -> Tuple[str, str]:
        d, f = os.path.split(self.doc)
        dest_dir = os.path.join('.', 'html', d[2:])
        dest = os.path.join(
            dest_dir,
            os.path.splitext(f)[0] + '.html')

        return dest_dir, dest


    def link_prev(self, prev_post: 'Post') -> None:
        self.prev = prev_post


    def link_next(self, next_post: 'Post') -> None:
        self.next = next_post


    def process_markdown(self, md: Callable[[str], str]) -> None:
        self.body = md(self.text)


def render_post(post: Post, template: templating.VerySimpleTemplate,
    md: Callable[[str], str], config: Dict[str, str]) -> None:
    post.process_markdown(md)

    dest_dir, dest = post.get_dest()

    utils.ensure_path(dest_dir)

    with utils.open_utf8(dest, 'w+') as f:
        # Make all config properties available to the template
        f.write(templating.render(template, {'post': post} | config))
