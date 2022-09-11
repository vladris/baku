from baku import utils
import html
import os


class Post:
    def __init__(self, doc):
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
        with open(doc, 'r') as f:
            self.text = f.read()

        # Relative path and link
        self.rel_path = (os.path.splitext(doc)[0] + '.html').replace(
            os.path.pathsep, '/')
        self.href = '../../../' + self.rel_path[2:]

        self.title = html.unescape(self.text.split('\n', 1)[0].strip(' #'))

        self.prev, self.next = None, None


    def link_prev(self, prev):
        self.prev = prev


    def link_next(self, next):
        self.next = next


    def process_markdown(self, md):
        self.body = md.process(self.text)


def render_post(post, template, md, config):
    post.process_markdown(md)
    
    utils.ensure_path(post.dest_dir)

    open(post.dest, 'w+').write(
        # Make all config properties available to the template
        template.render({'post': post} | config))
