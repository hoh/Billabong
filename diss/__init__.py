
import os
import hashlib
import magic
from base64 import b64encode, b64decode
from datetime import datetime

from .settings import inventory
from .encryption import random_key, copy_and_encrypt, decrypt_blob

hashing = hashlib.sha256


def add_file(filepath, *, key=None):
    "Import a file into Dis."

    # Resolve symlinks
    realpath = os.path.realpath(filepath)

    if not os.path.isfile(filepath):
        raise FileNotFoundError

    if key is None:
        key = random_key()

    file_hash = hashing()
    file_hash.update(open(filepath, 'rb').read())

    id_ = copy_and_encrypt(filepath, key)

    meta = {
        'key': b64encode(key),
        'hash': 'sha256-' + file_hash.hexdigest(),
        'size': os.path.getsize(realpath),
        'timestamp': datetime.now(),
        'id': id_,

        'info': {
            'type': magic.from_file(realpath).decode(),
            'mimetype': magic.from_file(realpath, mime=True).decode(),
            'filename': os.path.basename(filepath),
            'path': filepath,
            }
        }

    inventory.save_record(meta)

    return meta


def get_content(id_, *, offset=0, length=None):
    key = b64decode(inventory.get_record(id_)['key'])
    return decrypt_blob(id_, key, offset=offset, length=length)
