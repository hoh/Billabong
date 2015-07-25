# Copyright (c) 2015 "Hugo Herter http://hugoherter.com"
#
# This file is part of Billabong.
#
# Intercom is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""
Check the integrity of the data.
"""

import logging
from base64 import b64decode

from .encryption import hashing, decrypt_blob
from .utils import read_in_chunks
from .exceptions import CheckError
from .settings import inventory, stores


def compute_hash(file_object, chunk_size=1024):
    """Compute the hash of the content of a file object using
    the given hashing function.
    """
    file_hash = hashing()
    for chunk in read_in_chunks(file_object, chunk_size):
        file_hash.update(chunk)
    return file_hash


def check_data(id=None, meta=None, raises=False):

    if id and not meta:
        meta = inventory.get_record(id)
    elif meta and not id:
        id = meta['id']
    else:
        raise ValueError("Missing value for 'id' or 'meta'.")

    blob_id = meta['blob']
    check_enc_data(blob_id)

    key = b64decode(meta['key'])
    hash = meta['hash']
    check_clear_data(blob_id, key, hash)


def check_enc_data(blob_id, raises=False):
    "Check the validity of an encrypted blob"

    enc_path = stores[0]._blob_path(blob_id)
    with open(enc_path, 'rb') as enc_file:
        enc_hash = compute_hash(enc_file)

    if id != enc_hash.hexdigest():
        if raises:
            raise CheckError(
                "Data does not match the hash for id '{}'".format(id))
        else:
            logging.error(
                "Data does not match the hash for id '{}'".format(id))


def check_clear_data(id, key, hash):
    "Check the validity of the clear data inside a blob"

    clear_data = decrypt_blob(stores[0], id, key)

    clear_hash = hashing()
    for chunk in clear_data:
        clear_hash.update(chunk)

    if hash != "sha256-" + clear_hash.hexdigest():
        raise CheckError()
