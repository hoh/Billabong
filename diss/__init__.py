
import os
import hashlib
import magic
from datetime import datetime

from .settings import METADATA_PATH
from .meta import get_meta
from .encryption import copy_and_encrypt, decrypt_blob
from .utils import dumps

hashing = hashlib.sha256


def save_metadata(meta):
    destination = os.path.join(METADATA_PATH, meta['id'] + '.json')
    open(destination, 'w').write(dumps(meta))


def add_file(filepath):
    "Import a file into Dis."

    if not os.path.isfile(filepath):
        raise FileNotFoundError

    key = b'0'*32

    file_hash = hashing()
    file_hash.update(open(filepath, 'rb').read())

    # TODO: replace by a hash of the encrypted file
    id_ = copy_and_encrypt(filepath, key)

    meta = {
        'key': key,
        'hash': 'sha256-' + file_hash.hexdigest(),
        'size': os.path.getsize(filepath),
        'timestamp': datetime.now(),
        'id': id_,

        'info': {
            'type': magic.from_file(filepath).decode(),
            'mimetype': magic.from_file(filepath, mime=True).decode(),
            'filename': os.path.basename(filepath),
            'path': filepath,
            }
        }

    save_metadata(meta)

    return meta


def get_content(id_):
    key = get_meta(id_)['key']
    return decrypt_blob(id_, key)
