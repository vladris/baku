from baku import consts, templating
import os
import pyquery


def build_feed(posts, config):
    template = templating.VerySimpleTemplate(
        os.path.join('templates', consts.RSS_TEMPLATE))

    base_url = config['url'].strip('/')

    for post in posts:
        post.url = base_url + '/' + post.rel_path[2:]
        post.body = patch_links(base_url, post)

    open(
        os.path.join('.', 'html', 'rss.xml'),
        'w+').write(template.render({'posts': posts} | config))


def patch_links(base_url, post):
    doc = pyquery.PyQuery(post.body)
    abs_path = f'{base_url}/{post.year}/{post.month}/{post.day}/'

    # Patch img nodes
    for img in doc.find('img'):
        src = img.get('src', '')
        if not src.startswith('.'):
            src = abs_path + src
        img.set('src', src)

    # Patch a nodes
    for anchor in doc.find('a'):
        ref = anchor.get('href')
        # Skip anchor links (no href)
        if ref is not None:
            if ref.startswith('../'):
                ref = abs_path + ref[9:]

    return doc.html()
