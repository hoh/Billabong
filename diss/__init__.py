
import os
import magic
from uuid import uuid4
from base64 import b64encode, b64decode
from datetime import datetime

from .settings import inventory
from .encryption import random_key, copy_and_encrypt, decrypt_blob
from .check import compute_hash


def add_file(filepath, *, key=None):
    "Import a file into Dis."

    # Resolve symlinks
    realpath = os.path.realpath(filepath)

    if not os.path.isfile(filepath):
        raise FileNotFoundError

    if key is None:
        key = random_key()

    with open(filepath, 'rb') as source_file:
        file_hash = compute_hash(source_file)

    blob_hash = copy_and_encrypt(filepath, key)

    meta = {
        'key': b64encode(key),
        'hash': 'sha256-' + file_hash.hexdigest(),
        'blob': blob_hash,
        'size': os.path.getsize(realpath),
        'timestamp': datetime.now(),
        'id': uuid4().hex,

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
    record = inventory.get_record(id_)
    key = b64decode(record['key'])
    blob_id = record['blob']
    return decrypt_blob(blob_id, key, offset=offset, length=length)
