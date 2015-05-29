"""
Check the integrity of Diss data
"""

import os
import logging
from base64 import b64decode

from .encryption import hashing, decrypt_blob
from .meta import get_meta
from .utils import read_in_chunks
from .exceptions import CheckError
from .settings import STORAGE_PATH


def check_data(id=None, meta=None, raises=False):

    if id and not meta:
        meta = get_meta(id)
    elif meta and not id:
        id = meta['id']
    else:
        raise ValueError("Missing value for 'id' or 'meta'.")

    check_enc_data(id)

    key = b64decode(meta['key'])
    hash = meta['hash']
    check_clear_data(id, key, hash)


def check_enc_data(id, raises=False):
    "Check the validity of an encrypted blob"

    enc_path = os.path.join(STORAGE_PATH, id)
    enc_file = open(enc_path, 'rb')
    enc_hash = hashing()

    for enc_chunk in read_in_chunks(enc_file):
        enc_hash.update(enc_chunk)

    if id != enc_hash.hexdigest():
        if raises:
            raise CheckError(
                "Data does not match the hash for id '{}'".format(id))
        else:
            logging.error(
                "Data does not match the hash for id '{}'".format(id))


def check_clear_data(id, key, hash):
    "Check the validity of the clear data inside a blob"

    clear_data = decrypt_blob(id, key)

    clear_hash = hashing()
    for chunk in clear_data:
        clear_hash.update(chunk)

    if hash != "sha256-" + clear_hash.hexdigest():
        raise CheckError()
