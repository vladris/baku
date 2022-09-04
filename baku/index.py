from baku import consts, templating
from datetime import datetime
import misaka
import os

def build_index(posts):
    template = templating.Template(
        os.path.join('templates', consts.ROOT_TEMPLATE))

    html = '<div id="index">'
    year = ''
    for post in posts:
        if post.year != year:
            html += f'<div class="year"><span>{post.year}</span></div>'
            year = post.year

        month = datetime.strftime(post.date, '%b')

        html += f'<div class="date"><span>{month} {post.day}</span></div>' + \
            f'<div class="post"><span><a href="{post.rel_path}">' + \
            f'{misaka.escape_html(post.title)}</a></span></div>\n'

    html += '</div>'

    context = {'body': html}

    open(
        os.path.join('.', 'html', 'index.html'),
        'w+').write(template.render(context))
