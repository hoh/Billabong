
from diss.settings import storage, remote_storages
from diss.sync import push_blobs, push_blob
from .testdata import ID

remote = remote_storages[0]


def test_push_blobs():
    remote.delete_everything(confirm=True)
    push_blobs()
    remote.delete_everything(confirm=True)


def test_push_blob():
    remote.delete_everything(confirm=True)
    push_blob(ID, storage, remote)
    remote.delete_everything(confirm=True)
