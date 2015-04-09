
import os
import hashlib
from datetime import datetime

from diss.utils import dumps, loads

hashing = hashlib.sha256
STORAGE_PATH = './data'
METADATA_PATH = './meta'


def copy_file(meta):
    "Copy a file in the data storage"
    destination = os.path.join(STORAGE_PATH, meta['id'])
    open(destination, 'wb').write(open(meta['path']['absolute'], 'rb').read())


def save_metadata(meta):
    destination = os.path.join(METADATA_PATH, meta['id'] + '.json')
    open(destination, 'w').write(dumps(meta))


def add_file(filepath):
    "Import a file into Dis."

    if not os.path.isfile(filepath):
        raise FileNotFoundError

    key = 'UNIQUE_SECRET_KEY'

    meta = {
        'path': {'filename': filepath,
                 'absolute': filepath,
                 'relative': filepath,
                 },
        'key': key,
    }

    file_hash = hashing()
    file_hash.update(open(filepath, 'rb').read())
    meta['hash'] = 'sha256-' + file_hash.hexdigest()

    meta['timestamp'] = datetime.now()

    meta['id'] = hashing((key + meta['hash']).encode()).hexdigest()

    copy_file(meta)
    save_metadata(meta)

    return meta


def get_meta(id_):
    "Load metadata for the given id."
    filepath = os.path.join(METADATA_PATH, id_ + '.json')
    return loads(open(filepath, 'r').read())


def list_blobs():
    for id_ in os.listdir(METADATA_PATH):
        id_ = id_.replace('.json', '')
        meta = get_meta(id_)
        yield meta['path']['relative']


def get_content(id_):
    destination = os.path.join(STORAGE_PATH, id_)
    return open(destination).read()
