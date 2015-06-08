"""Blob Storage
"""

import os
from shutil import copyfileobj
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

    def import_blob(self, id_, filename):
        "Add an encrypted blob file to the storage"
        raise NotImplementedError

    def read_in_chunks(self, id_, chunk_size=1024):
        "Read a blob chunk by chunk"
        raise NotImplementedError

    def missing_from(self, other_storage):
        "Return the ids present locally but not on the other storage."
        blobs_self = set(self.list_blob_ids())
        blobs_other = set(other_storage.list_blob_ids())
        return blobs_self - blobs_other

    def push_to(self, other_storage):
        "Push local blobs to another storage"
        raise NotImplementedError

    def push_blob_to(self, id_, other_storage):
        "Push a local blob to another storage."
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

    def import_blob(self, id_, blobfile):
        "Add an encrypted blob file to the storage by copying the file."
        copyfileobj(blobfile,
                    open(self._blob_path(id_), 'wb'))

    def read_in_chunks(self, id_, offset=0, chunk_size=1024):
        "Read a blob file chunk by chunk."
        path = self._blob_path(id_)
        fd = open(path, 'rb')
        fd.seek(offset)
        return enumerate(read_in_chunks(fd, chunk_size))

    def push_to(self, other_storage):
        "Push local blobs to another storage"
        for id_ in self.missing_from(other_storage):
            self.push_blob_to(id_, other_storage)

    def push_blob_to(self, id_, other_storage):
        "Push a local blob to another storage"
        blobfile = open(self._blob_path(id_), 'rb')
        other_storage.import_blob(id_, blobfile)
