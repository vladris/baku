import os
import shutil
from typing import Dict, List
from baku import consts, index, environment, markdown, post, rss, templating, utils


def clean_dest() -> None:
    print('Cleaning up destination', end=' ')
    if os.path.exists('html'):
        shutil.rmtree('html')
    utils.ensure_path('html')
    print('✅')


def collect_files() -> List[post.Post]:
    print('Collecting files', end=' ')
    posts, assets = [], []
    for root, _, files in os.walk('.'):
        # Ignore root, drafts, html, templates
        if root in [
            '.',
            os.path.join('.', 'drafts'),
            os.path.join('.', 'html'),
            os.path.join('.', 'templates')]:
            continue

        # Ignore dot directories
        if root.startswith(os.path.join('.', '.')):
            continue

        for f in files:
            if os.path.splitext(f)[1] == '.md':
                posts.append(post.Post(os.path.join(root, f)))
            else:
                assets.append(os.path.join(root, f))

    print(f'✅ ({len(posts)} post(s), {len(assets)} asset(s))')
    return sorted(posts, key=lambda p: p.doc, reverse=True), \
        sorted(assets, reverse=True)


def get_dest(source: str) -> str:
    return os.path.join(
        '.', 'html', os.path.split(source[2:])[0])


def render_posts(posts: List[post.Post], config: Dict[str, str]) -> None:
    print('Rendering posts...', end=' ')
    template = templating.VerySimpleTemplate(
        os.path.join('templates', consts.POST_TEMPLATE))
    md = markdown.make_markdown_processor()

    for i, p in enumerate(posts):
        if i > 0:
            p.link_next(posts[i - 1])
        if i < len(posts) - 1:
            p.link_prev(posts[i + 1])

        post.render_post(p, template, md, config)

    print('✅')


def build_index(posts: List[post.Post], config: Dict[str, str]) -> None:
    print('Generating index.html...', end=' ')
    index.build_index(posts, config)
    print('✅')


def copy_assets(assets: List[str]) -> None:
    print('Copying assets...', end=' ')
    for asset in assets:
        dest = get_dest(asset)
        utils.ensure_path(dest)
        shutil.copy(asset, dest)
    print('✅')


def build_rss_feed(posts: List[post.Post], config: Dict[str, str]) -> None:
    print('Building RSS feed...', end=' ')
    rss.build_feed(posts, config)
    print('✅')


def build() -> None:
    clean_dest()
    posts, assets = collect_files()
    config = environment.load_config()
    render_posts(posts, config)
    build_index(posts, config)
    copy_assets(assets)
    build_rss_feed(posts, config)
