import os
from typing import List, Dict
from baku import consts, post, templating, utils


def build_index(posts: List[post.Post], config: Dict[str, str]):
    template = templating.VerySimpleTemplate(
        os.path.join('templates', consts.ROOT_TEMPLATE))

    # Group posts by year
    posts_by_year, context = {}, {'years': []}
    for p in posts:
        if p.date.year not in posts_by_year:
            posts_by_year[p.date.year] = []

        posts_by_year[p.date.year].append(p)

    # Generate context
    for year in sorted(posts_by_year.keys(), reverse=True):
        context['years'].append({
            'year': year,
            'posts': posts_by_year[year]
        })

    with utils.open_utf8(os.path.join('.', 'html', 'index.html'), 'w+') as f:
        f.write(templating.render(template, context | config))
