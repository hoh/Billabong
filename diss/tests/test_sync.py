import os

from diss.settings import REMOTE_LOCATION
from diss.sync import push_blobs, push_blob
from .testdata import ID


def empty_remote():
    for i in os.listdir(REMOTE_LOCATION):
        os.remove(os.path.join(REMOTE_LOCATION, i))


def test_push_blobs():
    empty_remote()
    push_blobs()
    empty_remote()


def test_push_blob():
    empty_remote()
    push_blob(ID)
    empty_remote()
