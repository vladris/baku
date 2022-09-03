import misaka as m
import os
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name


# Syntax highlighting
class HighlighterRenderer(m.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)

        return '\n<pre><code>{}</code></pre>\n'.format(
                            m.escape_html(text.strip()))


class Post:
    def __init__(self, doc):
        self.doc = doc
        self.dest = os.path.splitext(doc)[0] + '.html'
        self.text = open(doc, 'r').read()
        self.title = self.text.split('\n', 1)[0].strip('# ')


    def __str__(self):
        return f'{self.doc} -> {self.dest} / {self.title}' 


def build():
    renderer = HighlighterRenderer()
    md = m.Markdown(renderer, extensions=('fenced-code', 'footnotes', 'math', 'math-explicit', 'quote', 'tables'))

    posts = []

    for root, _, files in os.walk('.'):
        for f in files:
            name, ext = os.path.splitext(f)

            # We only care about Markdown files
            if ext != '.md':
                continue

            # Ignore drafts
            if root == os.path.join('.', 'drafts'):
                continue

            posts.append(Post(os.path.join(root, f)))

    for i, post in enumerate(posts):
        print(f'Building {post.dest}', end='')
        render(post, posts[i - 1] if i > 0 else None, posts[i + 1] if i < len(posts) - 1 else None, md)
        print(' ✅')


def render(post, next, prev, md):
    html = md(open(post.doc, 'r').read())
    template = open(os.path.join('templates', 'post.html'), 'r').read()

    # Link next post
    if next:
        href = os.path.join('../../..', next.dest)
        text = m.escape_html(next.title)
        template = template.replace('$$NEXT$$', f'<a href={href}>{text}</a>')
    else:
        template = template.replace('$$NEXT$$', '')

    # Link previous post
    if prev:
        href = os.path.join('../../..', prev.dest)
        text = m.escape_html(prev.title)
        template = template.replace('$$PREV$$', f'<a href={href}>{text}</a>')
    else:
        template = template.replace('$$PREV$$', '')

    # Insert title
    template = template.replace('$$TITLE$$', post.title)
    
    # Insert body
    template = template.replace('$$BODY$$', html)

    open(post.dest, 'w+').write(template)
