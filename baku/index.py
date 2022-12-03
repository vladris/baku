import os
from itertools import groupby
from typing import List, Dict
from baku import consts, post, templating, utils


def build_index(posts: List[post.Post], config: Dict[str, str]):
    template = templating.VerySimpleTemplate(
        os.path.join('templates', consts.ROOT_TEMPLATE))

    # Group posts by year
    context = {'years': []}
    for year, posts_generator in groupby(sorted(posts, key=lambda x: x.date, reverse=True), key=lambda x: x.date.year):
        context['years'].append({
            'year': year,
            'posts': list(posts_generator)
        })

    with utils.open_utf8(os.path.join('.', 'html', 'index.html'), 'w+') as f:
        f.write(templating.render(template, context | config))
