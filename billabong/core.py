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

import os.path
from uuid import uuid4
from base64 import b64encode, b64decode
from datetime import datetime

import magic

from .encryption import random_key, copy_and_encrypt, decrypt_blob
from .check import compute_hash


class Billabong:

    """High-level interface above inventory and storages."""

    def __init__(self, inventory, stores):
        self.inventory = inventory
        self.stores = stores

    def add_file(self, filepath, *, key=None):
        """Import a file into Billabong and return the corresponding record."""
        # Resolve symlinks
        realpath = os.path.realpath(filepath)

        if not os.path.isfile(realpath):
            raise FileNotFoundError

        if key is None:
            key = random_key()

        with open(realpath, 'rb') as source_file:
            file_hash = compute_hash(source_file)

        storage = self.stores[0]
        blob_hash = copy_and_encrypt(storage, realpath, key)

        record = {
            'key': b64encode(key).decode(),
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

        self.inventory.save_record(record)
        return record

    def get(self, id_):
        """Return a Record object from an id_."""
        return self.inventory.get_record(id_)

    def delete(self, id_):
        """Delete a Record and the corresponding blob."""
        blob_id = self.inventory.get_record(id_)['blob']
        for store in self.stores:
            store.delete(blob_id)
        self.inventory.delete(id_)

    def read(self, id_, length=None, offset=0, chunk_size=1024):
        """Return data from the blob of this file."""
        record = self.inventory.get_record(id_)
        key = b64decode(record['key'])
        blob_id = record['blob']

        for store in self.stores:
            if store.contains(blob_id):
                return decrypt_blob(store, blob_id, key,
                                    offset=offset, length=length)
        else:
            raise FileNotFoundError
