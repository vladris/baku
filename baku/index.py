import os
from typing import List, Dict
from baku import consts, post, templating, utils


def build_index(posts: List[post.Post], config: Dict[str, str]):
    template = templating.VerySimpleTemplate(
        os.path.join('templates', consts.ROOT_TEMPLATE))

    # Group posts by year
    year, context, posts_in_year = posts[0].year, {'years': []}, []
    for p in posts:
        if p.year == year:
            posts_in_year.append(p)
        else:
            context['years'].append({
                'year': year,
                'posts': posts_in_year
            })
            year, posts_in_year = p.year, [p]

    with utils.open_utf8(os.path.join('.', 'html', 'index.html'), 'w+') as f:
        f.write(template.render(context | config))
