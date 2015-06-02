"""Blob Storage
"""

import os


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
