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

"""Storage implementation based on the HTTP protocol."""


import os.path
import http.client
from urllib.parse import urlparse

from .abstract import Storage


class HTTPStorage(Storage):

    """Blob storage on a remote read-only HTTP(S) host."""

    def __init__(self, url):
        """Initialize an HTTP storage based on the given root url."""
        self.url = url

    def contains(self, id_):
        """Return if the given blob id is present in the storage."""
        u = urlparse(self.url)
        conn = http.client.HTTPConnection(host=u.hostname,
                                          port=u.port)
        conn.request('HEAD', os.path.join(u.path, id_))
        resp = conn.getresponse()
        return (resp.status == 200)


    def read_in_chunks(self, id_, offset=0, chunk_size=1024):
        """Read a blob file from HTTP chunk by chunk."""
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
