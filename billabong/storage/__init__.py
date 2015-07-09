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


"""Blob Storage
"""

import os
from shutil import copyfileobj
from billabong.utils import read_in_chunks

from urllib.parse import urlparse
import http.client


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

    def delete(self, blob_id):
        "Delete a blob from the storage"
        os.remove(self._blob_path(blob_id))

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


class HTTPStorage(Storage):
    """Blob storage on a remote read-only HTTP(S) host
    """

    def __init__(self, url):
        self.url = url

    def read_in_chunks(self, id_, offset=0, chunk_size=1024):
        "Read a blob file from HTTP chunk by chunk"
        print('read http chunk {} {}'.format(id_, offset))

        u = urlparse(self.url)
        conn = http.client.HTTPConnection(host=u.hostname,
                                          port=u.port)
        conn.request('GET', os.path.join(u.path, id_),
                     headers={'Range': 'bytes={}-'.format(offset)})
        resp = conn.getresponse()

        if resp.status == 206:
            # 206 = Partial Content
            i = 0
            chunk = resp.read(chunk_size)
            while chunk:
                yield i, chunk
                chunk = resp.read(chunk_size)
                i += 1

        elif resp.status == 404:
            raise ValueError("404 not found")
        else:
            raise NotImplementedError("Range unsupported, status {}"
                                      .format(resp.status))


def load_storage(settings):
    type_ = settings['type']
    args = settings.get('args', {})

    if type_ == 'FolderStorage':
        return FolderStorage(**args)
    elif type_ == 'HTTPStorage':
        return HTTPStorage(**args)
