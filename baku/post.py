import html
import os
from typing import Callable, Dict
from baku import utils
from baku.templating import VerySimpleTemplate


class Post:
    def __init__(self, doc: str):
        self.doc = doc

        # Timestamp
        _, self.year, self.month, self.day, _ = doc.split(os.path.sep)
        self.date = utils.parse_date(
            f'{self.year}/{self.month}/{self.day}').astimezone()

        # Destination directory and file
        d, f = os.path.split(doc)
        self.dest_dir = os.path.join('.', 'html', d[2:])
        self.dest = os.path.join(
            self.dest_dir,
            os.path.splitext(f)[0] + '.html')

        # Load content
        with utils.open_utf8(doc, 'r') as f:
            self.text = f.read()

        # Relative path and link
        self.rel_path = (os.path.splitext(doc)[0] + '.html').replace(
            os.path.pathsep, '/')
        self.href = '../../../' + self.rel_path[2:]

        self.title = html.unescape(self.text.split('\n', 1)[0].strip(' #'))

        self.prev, self.next, self.body = None, None, None


    def link_prev(self, prev_post: 'Post') -> None:
        self.prev = prev_post


    def link_next(self, next_post: 'Post') -> None:
        self.next = next_post


    def process_markdown(self, md: Callable[[str], str]) -> None:
        self.body = md(self.text)


def render_post(post: Post, template: VerySimpleTemplate,
    md: Callable[[str], str], config: Dict[str, str]) -> None:
    post.process_markdown(md)

    utils.ensure_path(post.dest_dir)

    with utils.open_utf8(post.dest, 'w+') as f:
        # Make all config properties available to the template
        f.write(template.render({'post': post} | config))
