
from os import listdir
from shutil import copy2
from os import path

from .settings import STORAGE_PATH, REMOTE_LOCATION
from .meta import list_records


def push_blobs():
    records_local = set(list_records())
    records_remote = set(list_remote_records())
    to_sync = records_local - records_remote

    print('records_local', records_local)
    print('records_remote', records_remote)
    print('to_sync', to_sync)

    for id_ in to_sync:
        push_blob(id_)


def list_remote_records():
    return listdir(REMOTE_LOCATION)


def push_blob(id_):
    print('pushing blob', id_)
    path_local = path.join(STORAGE_PATH, id_)
    path_remote = path.join(REMOTE_LOCATION, id_)
    copy2(path_local, path_remote)
