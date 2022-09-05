from baku import consts, index, environment, markdown, post, templating, utils
import os
import shutil


def clean_dest():
    print('Cleaning up destination', end=' ')
    if os.path.exists('html'):
        shutil.rmtree('html')
    utils.ensure_path('html')
    print('✅')


def collect_files():
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


def get_dest(source):
    return os.path.join(
        '.', 'html', os.path.split(source[2:])[0])


def render_posts(posts):
    print('Rendering posts...', end=' ')
    template = templating.Template(
        os.path.join('templates', consts.POST_TEMAPLTE))
    md = markdown.Markdown()
    config = environment.load_config()

    for i, p in enumerate(posts):
        if i > 0:
            p.link_next(posts[i - 1])
        if i < len(posts) - 1:
            p.link_prev(posts[i + 1])

        post.render_post(p, template, md, config)

    print('✅')

    
def build_index(posts):
    print('Generating index.html...', end=' ')
    index.build_index(posts)
    print('✅')


def copy_assets(assets):
    print('Copying assets...', end=' ')
    for asset in assets:
        dest = get_dest(asset)
        utils.ensure_path(dest)
        shutil.copy(asset, dest)
    print('✅')


def build():
    clean_dest()
    posts, assets = collect_files()
    render_posts(posts)
    build_index(posts)
    copy_assets(assets)
