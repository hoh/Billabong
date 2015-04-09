
import os
import hashlib
import magic
from datetime import datetime

from diss.utils import dumps, loads

hashing = hashlib.sha256
STORAGE_PATH = './data'
METADATA_PATH = './meta'


def copy_file(meta):
    "Copy a file in the data storage"
    destination = os.path.join(STORAGE_PATH, meta['id'])
    open(destination, 'wb').write(open(meta['info']['path'], 'rb').read())


def save_metadata(meta):
    destination = os.path.join(METADATA_PATH, meta['id'] + '.json')
    open(destination, 'w').write(dumps(meta))


def add_file(filepath):
    "Import a file into Dis."

    if not os.path.isfile(filepath):
        raise FileNotFoundError

    key = 'UNIQUE_SECRET_KEY'

    file_hash = hashing()
    file_hash.update(open(filepath, 'rb').read())

    meta = {
        'key': key,
        'hash': 'sha256-' + file_hash.hexdigest(),
        'size': os.path.getsize(filepath),
        'timestamp': datetime.now(),
        'id': hashing((key + file_hash.hexdigest()).encode()).hexdigest(),

        'info': {
            'type': magic.from_file(filepath).decode(),
            'mimetype': magic.from_file(filepath, mime=True).decode(),
            'filename': filepath,
            'path': filepath,
            }
        }


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
        yield meta['info']['path']


def get_content(id_):
    destination = os.path.join(STORAGE_PATH, id_)
    return open(destination).read()
