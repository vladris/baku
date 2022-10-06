from typing import Callable
import misaka as m
from pygments import highlight
from pygments.formatters import ClassNotFound
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name


# Syntax highlighting
class HighlighterRenderer(m.HtmlRenderer):
    # pylint: disable=too-few-public-methods
    # This is what Misaka wants to enable Pygments
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)

        return f'\n<pre><code>{m.escape_html(text.strip())}</code></pre>\n'


def make_markdown_processor() -> Callable[[str], str]:
    return m.Markdown(HighlighterRenderer(),
        extensions=(
            'fenced-code',
            'footnotes',
            'math',
            'math-explicit',
            'quote',
            'tables'))
