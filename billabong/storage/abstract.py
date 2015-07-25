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

"""Abstract interface for storage implemenations."""


class Storage:

    """Storage interface to implement.

    A Blob Storage represents a location where encrypted blobs can be stored
    and synced from/to.
    """

    def list_blob_ids(self):
        """Get the ids of all blobs in the storage."""
        raise NotImplementedError

    def contains(self, id_):
        """Return if the given blob id is present in the storage."""
        return id_ in self.list_blob_ids()

    def delete(self, id_):
        """Delete a given blob in the storage."""
        raise NotImplementedError

    def delete_everything(self):
        """Delete every blob from the storage."""
        for blob_id in self.list_blob_ids():
            self.delete(blob_id)

    def import_blob(self, id_, blobfile, callback=None):
        """Add an encrypted blob file to the storage."""
        raise NotImplementedError

    def read_in_chunks(self, id_, offset=0, chunk_size=1024):
        """Read a blob chunk by chunk."""
        raise NotImplementedError

    def missing_from(self, other_storage):
        """Get the ids present locally but not on an other storage."""
        blobs_self = set(self.list_blob_ids())
        blobs_other = set(other_storage.list_blob_ids())
        return blobs_self - blobs_other

    def push_to(self, other_storage):
        """Push local blobs to another storage."""
        raise NotImplementedError

    def push_blob_to(self, id_, other_storage):
        """Push a local blob to another storage."""
        raise NotImplementedError
