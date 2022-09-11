from baku import consts, templating
import os


def build_index(posts, config):
    template = templating.VerySimpleTemplate(
        os.path.join('templates', consts.ROOT_TEMPLATE))

    # Group posts by year
    year, context, posts_in_year = posts[0].year, {'years': []}, []
    for post in posts:
        if post.year == year:
            posts_in_year.append(post)
        else:
            context['years'].append({
                'year': year,
                'posts': posts_in_year
            })
            year, posts_in_year = post.year, [post]

    open(
        os.path.join('.', 'html', 'index.html'),
        'w+').write(template.render(context | config))
