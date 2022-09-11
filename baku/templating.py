from datetime import datetime
import html
from types import SimpleNamespace as sn


class VerySimpleTemplate:
    def __init__(self, file):
        with open(file, 'r') as f:
            text = f.read()
        self.template, _ = self.__parse(text)
    

    def render(self, context):
        return self.__walk(self.template, context)
    

    def __parse(self, text, pos=0, stop=None):
        nodes, p = [], pos
        while True:
            # Parse raw text
            n, p = self.__parseText(text, p)
            if n.value:
                nodes.append(n)

            if p == -1:
                break

            # Parse an expression
            n, p = self.__parseExpr(text, p)
            if n.expr == stop:
                break

            nodes.append(n)

        # Return a list node
        return sn(type='list', children=nodes), p


    def __parseText(self, text, pos):
        # Text ends when '{{' is encountered (or end of string)
        p = text.find('{{', pos)
        value = text[pos:p] if p != -1 else text[pos:]
        
        # Return a text node
        return sn(type='text', value=value), p


    def __parseExpr(self, text, pos):
        # Expression ends when '}}' is encountered
        p = text.find('}}', pos) + 2
        expr = text[pos + 2:p - 2].strip()
        if expr.startswith('if '):
            # Parse list until an endif expression
            branch, p = self.__parse(text, p, 'endif')
            
            # Return an if node
            return sn(type='if', expr=expr[3:].strip(), branch=branch), p
        elif expr.startswith('for '):
            # Parse list until an endfor expression
            loop, p = self.__parse(text, p, 'endfor')
            
            # Return a for node
            return sn(type='for', expr=expr[4:].strip(), loop=loop), p
        else:
            # Return an expression node
            return sn(type='expr', expr=expr), p


    def __get(self, expr, context):
        # If context is a dictionary, treat expr as key, else as an attribute
        return context[expr] if isinstance(context, dict) \
            else context.__getattribute__(expr)


    def __eval(self, expr, context):
        # If just an identifier, return value from context
        if '.' not in expr:
            # ~ applies date formatting
            if '~' in expr:
                expr, fmt = expr.split('~', 1)
                return datetime.strftime(
                    self.__get(expr.strip(), context), fmt.strip())
            # & does an HTML escape on the value
            if '&' in expr:
                expr, _ = expr.split('&', 1)
                return html.escape(
                    str(self.__get(expr.strip(), context)))

            return self.__get(expr, context)

        # Split attribute addressing and evaluate recursively
        head, tail = expr.split('.', 1)
        return self.__eval(tail, self.__get(head, context))


    def __walk(self, node, context):
        match node.type:
            case 'text':
                return node.value
            case 'expr':
                return str(self.__eval(node.expr, context))
            case 'list':
                return ''.join([self.__walk(n, context) for n in node.children])
            case 'if':
                if self.__eval(node.expr, context):
                    return self.__walk(node.branch, context)
                else:
                    return ''
            case 'for':
                return ''.join([self.__walk(node.loop, context | {'$item':
                    item}) for item in self.__eval(node.expr, context)])
