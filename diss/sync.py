
from shutil import copy2
from .settings import storage, remote_storages


def push_blobs():
    for remote in remote_storages:
        storage.push_to(remote)


def push_blob(blob_id, storage, remote):
    print('pushing blob', blob_id)
    path_local = storage._blob_path(blob_id)
    path_remote = remote._blob_path(blob_id)
    copy2(path_local, path_remote)


def pull_blobs():
    for remote in remote_storages:
        remote.push_to(storage)
