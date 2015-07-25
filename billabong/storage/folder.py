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

"""Storage implementation based on the filesystem."""

import os
from shutil import copyfileobj

from billabong.utils import read_in_chunks
from .abstract import Storage


class FolderStorage(Storage):

    """Blob Storage in a folder accessible via the local filesystem."""

    def __init__(self, path):
        """Initialize a Folder storage based on the given path."""
        self.path = path

    def _blob_path(self, id_):
        """Get the path on the filesystem where a blob is stored."""
        return os.path.join(self.path, id_)

    def list_blob_ids(self):
        """List all ids present in the blobs storage."""
        for id_ in os.listdir(self.path):
            yield id_

    def delete(self, blob_id):
        """Delete a blob from the storage."""
        os.remove(self._blob_path(blob_id))

    def import_blob(self, id_, blobfile, callback=None):
        """Add an encrypted blob file to the storage by copying the file."""
        copyfileobj(blobfile,
                    open(self._blob_path(id_), 'wb'))
        if callback:
            callback()

    def read_in_chunks(self, id_, offset=0, chunk_size=1024):
        """Read a blob file chunk by chunk."""
        path = self._blob_path(id_)
        fdesc = open(path, 'rb')
        fdesc.seek(offset)
        return enumerate(read_in_chunks(fdesc, chunk_size))

    def push_to(self, other_storage):
        """Push local blobs to another storage."""
        for id_ in self.missing_from(other_storage):
            self.push_blob_to(id_, other_storage)

    def push_blob_to(self, id_, other_storage):
        """Push a local blob to another storage."""
        blobfile = open(self._blob_path(id_), 'rb')
        other_storage.import_blob(id_, blobfile)
