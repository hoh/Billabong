"""Blob Storage
"""

import os
from .utils import read_in_chunks


class Storage:
    """A Blob Storage represents a location where encrypted blobs can be stored
    and synced from/to.
    """

    def list_blob_ids(self):
        raise NotImplementedError

    def delete(self, id_):
        raise NotImplementedError

    def delete_everything(self, *, confirm=False):
        "Delete every blob from the storage"
        for blob_id in self.list_blob_ids():
            self.delete(blob_id)

    def import_file(self, filename):
        "Add an encrypted blob file to the storage"
        raise NotImplementedError

    def read_in_chunks(self, id_, chunk_size=1024):
        "Read a blob chunk by chunk"
        raise NotImplementedError


class FolderStorage(Storage):
    """Blob Storage in a folder accessible via the local filesystem.
    """

    def __init__(self, path):
        self.path = path

    def _blob_path(self, id_):
        "Returns the path on the filesystem where a blob is stored."
        return os.path.join(self.path, id_)

    def list_blob_ids(self):
        "List all ids present in the blobs storage."
        for id_ in os.listdir(self.path):
            yield id_

    def delete(self, id_):
        "Delete a blob from the storage"
        os.remove(self._blob_path(id_))

    def import_file(self, filepath, id_):
        "Add an encrypted blob file to the storage by moving the file."
        os.rename(filepath, self._blob_path(id_))

    def read_in_chunks(self, id_, offset=0, chunk_size=1024):
        "Read a blob file chunk by chunk."
        path = self._blob_path(id_)
        fd = open(path, 'rb')
        fd.seek(offset)
        return enumerate(read_in_chunks(fd, chunk_size))
