import misaka as m
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


class Markdown:
    def __init__(self):
        self.md = m.Markdown(HighlighterRenderer(),
            extensions=(
                'fenced-code',
                'footnotes',
                'math',
                'math-explicit',
                'quote',
                'tables'))


    def process(self, text):
        return self.md(text)