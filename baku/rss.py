import os
from typing import Dict, List
import pyquery
from baku import consts, post, templating, utils


def build_feed(posts: List[post.Post], config: Dict[str, str]) -> None:
    template = templating.VerySimpleTemplate(
        os.path.join('templates', consts.RSS_TEMPLATE))

    base_url = config['url'].strip('/')

    for p in posts:
        p.url = base_url + '/' + p.rel_path[2:]
        p.body = patch_links(base_url, p)

    with utils.open_utf8(os.path.join('.', 'html', 'rss.xml'), 'w+') as f:
        f.write(template.render({'posts': posts} | config))


def patch_links(base_url: str, p: post.Post) -> str:
    doc = pyquery.PyQuery(p.body)
    abs_path = f'{base_url}/{p.year}/{p.month}/{p.day}/'

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
