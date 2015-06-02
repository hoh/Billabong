"""Blob Storage
"""

import os
from .settings import STORAGE_PATH


def list_blobs():
    "List all ids present in the blobs storage."
    for id_ in os.listdir(STORAGE_PATH):
        yield id_


def delete_blob(id_):
    os.remove(os.path.join(STORAGE_PATH, id_))
