import os
import shutil
from baku import consts, utils

class Document():
    def __init__(self, title, path):
        self.title = title
        self.name = utils.name_from_title(title)

        # create post directory if it doesn't exist and get post path
        self.path = os.path.join(
            utils.ensure_path(path),
            self.name) + consts.SOURCE_SUFFIX


    def write(self):
        with open(self.path, "w+") as f:
            f.write(f'# {self.title}\n\n')


def create_document(title, path):
    doc = Document(title, path)
    if os.path.exists(doc.path):
        raise Exception(f'Document {title} already exists at {doc.path}')

    doc.write()
    return doc


def create_draft(title):
    return create_document(title, 'drafts')


def move(source, dest):
    dest_file = os.path.join(dest, os.path.split(source)[-1])
    if os.path.exists(dest_file):
        raise Exception(f'Document {dest_file} already exists')
    shutil.move(source, dest)
    return dest_file
