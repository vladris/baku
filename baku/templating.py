from dataclasses import dataclass
from datetime import datetime
import html
from types import SimpleNamespace as sn
from typing import Dict
from baku import utils


def _parse(text: str, pos: int = 0, stop: str = None) -> sn:
    nodes, p = [], pos
    while True:
        # Parse raw text
        n, p = _parse_text(text, p)
        if n.value:
            nodes.append(n)

        if p == -1:
            break

        # Parse an expression
        n, p = _parse_expr(text, p)
        if n.expr == stop:
            break

        nodes.append(n)

    # Return a list node
    return sn(type='list', children=nodes), p


def _parse_text(text: str, pos: int) -> sn:
    # Text ends when '{{' is encountered (or end of string)
    p = text.find('{{', pos)
    value = text[pos:p] if p != -1 else text[pos:]

    # Return a text node
    return sn(type='text', value=value), p


def _parse_expr(text: str, pos: int) -> sn:
    # Expression ends when '}}' is encountered
    p = text.find('}}', pos) + 2
    expr = text[pos + 2:p - 2].strip()
    if expr.startswith('if '):
        # Parse list until an endif expression
        branch, p = _parse(text, p, 'endif')

        # Return an if node
        return sn(type='if', expr=expr[3:].strip(), branch=branch), p

    if expr.startswith('for '):
        # Parse list until an endfor expression
        loop, p = _parse(text, p, 'endfor')

        # Return a for node
        return sn(type='for', expr=expr[4:].strip(), loop=loop), p

    # Return an expression node
    return sn(type='expr', expr=expr), p


def _get(expr: str, context: Dict[str, str]) -> str:
    # If context is a dictionary, treat expr as key, else as an attribute
    return context[expr] if isinstance(context, dict) \
        else getattr(context, expr)


def _eval(expr: str, context: Dict[str, str]) -> str:
    # If just an identifier, return value from context
    if '.' not in expr:
        # ~ applies date formatting
        if '~' in expr:
            expr, fmt = expr.split('~', 1)
            return datetime.strftime(
                _get(expr.strip(), context), fmt.strip())
        # & does an HTML escape on the value
        if '&' in expr:
            expr, _ = expr.split('&', 1)
            return html.escape(
                str(_get(expr.strip(), context)))

        return _get(expr, context)

    # Split attribute addressing and evaluate recursively
    head, tail = expr.split('.', 1)
    return _eval(tail, _get(head, context))


def _walk(node: sn, context: Dict[str, str]) -> str:
    match node.type:
        case 'text':
            return node.value
        case 'expr':
            return str(_eval(node.expr, context))
        case 'list':
            return ''.join([_walk(n, context) for n in node.children])
        case 'if':
            return _walk(node.branch, context) if \
                _eval(node.expr, context) else ''
        case 'for':
            return ''.join([_walk(node.loop, context | {'$item':
                item}) for item in _eval(node.expr, context)])


@dataclass
class VerySimpleTemplate:
    def __init__(self, file: str):
        with utils.open_utf8(file, 'r') as f:
            text = f.read()
        self.template, _ = _parse(text)


def render(template: VerySimpleTemplate, context: Dict[str, str]) -> str:
    return _walk(template.template, context)
