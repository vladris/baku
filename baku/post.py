from baku import utils
from datetime import datetime
import misaka
import os


class Post:
    def __init__(self, doc):
        self.doc = doc
        
        # Timestamp
        _, self.year, self.month, self.day, _ = doc.split(os.path.sep)
        self.date = datetime.strptime(
            f'{self.year}/{self.month}/{self.day}', '%Y/%m/%d')
        
        # Destination directory and file
        d, f = os.path.split(doc)
        self.dest_dir = os.path.join('.', 'html', d[2:])
        self.dest_file = os.path.splitext(f)[0] + '.html'
        self.dest = os.path.join(self.dest_dir, self.dest_file)

        # Relative path
        self.rel_path = os.path.splitext(doc)[0] + '.html'

        # Title and content
        self.text = open(doc, 'r').read()
        self.title = self.text.split('\n', 1)[0].strip('# ')

        # Previous and next links
        self.prev, self.next = None, None


    def link_prev(self, prev):
        self.prev = prev


    def link_next(self, next):
        self.next = next


def render_post(post, template, md, config):
    context = {}

    context['date'] = datetime.strftime(post.date, '%B %d, %Y')
    context['title'] = misaka.escape_html(post.title)

    # Link next post
    context['next'] = ''
    if post.next:
        href = os.path.join('../../..', post.next.rel_path)
        text = misaka.escape_html(post.next.title)
        context['next'] = f'<span><a href={href}>{text}</a> »</span>'

    # Link previous post
    context['prev'] = ''
    if post.prev:
        href = os.path.join('../../..', post.prev.rel_path)
        text = misaka.escape_html(post.prev.title)
        context['prev'] = f'<span>« <a href={href}>{text}</a></span>'

    context['body'] = md.process(post.text)
    
    # Make all config properties available to the template
    for key in config:
        context[key] = config[key]

    utils.ensure_path(post.dest_dir)
    open(post.dest, 'w+').write(template.render(context))
