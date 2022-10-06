from dataclasses import dataclass
from datetime import datetime
import os
import shutil
from baku import consts, utils

@dataclass
class Document():
    def __init__(self, title: str, path: str):
        self.title = title
        self.name = utils.name_from_title(title)

        # create post directory if it doesn't exist and get post path
        self.path = os.path.join(
            utils.ensure_path(path),
            self.name) + consts.SOURCE_SUFFIX


def create_document(title: str, path: str) -> Document:
    doc = Document(title, path)
    if os.path.exists(doc.path):
        raise Exception(f'Document {title} already exists at {doc.path}')

    with utils.open_utf8(doc.path, "w+") as f:
        f.write(f'# {doc.title}\n\n')

    return doc


def create_draft(title: str) -> Document:
    return create_document(title, 'drafts')


def move(source: str, dest: str) -> str:
    utils.ensure_path(dest)
    dest_file = os.path.join(dest, os.path.split(source)[-1])
    if os.path.exists(dest_file):
        raise Exception(f'Document {dest_file} already exists')
    shutil.move(source, dest)
    return dest_file


def create_or_move_post(title: str, date: datetime) -> None:
    path = utils.path_from_date(date)

    # If file exists as draft, promote it to a post
    if os.path.exists(title):
        new_post = move(title, path)
        print(f'Draft moved to post {new_post}')
    # Otherwise create a new post
    else:
        new_post = create_document(title, path)
        print(f'New post created as {new_post.path}')


def create_or_move_draft(title: str) -> None:
    # If file exists as post, move it to a draft
    if os.path.exists(title):
        new_draft = move(title, 'drafts')
        print(f'File moved to draft {new_draft}')
    # Otherwise create a new draft
    else:
        new_draft = create_draft(title)
        print(f'New draft created as {new_draft.path}')
