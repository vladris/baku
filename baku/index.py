from baku import consts, templating
from datetime import datetime
import misaka
import os

def build_index(posts):
    template = templating.Template(
        os.path.join('templates', consts.ROOT_TEMPLATE))

    html = ''
    year = ''
    for post in posts:
        if post.year != year:
            html += f'<h2>{post.year}</h2>'
            year = post.year

        month = datetime.strftime(post.date, '%b')

        html += f'<p>{month} {post.day} <a href={post.rel_path}>' + \
            f'{misaka.escape_html(post.title)}</a></p>\n'

    context = {'body': html}

    open(
        os.path.join('.', 'html', 'index.html'),
        'w+').write(template.render(context))
