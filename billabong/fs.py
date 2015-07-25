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


"""FUSE file system over the blob system."""

import errno

from fuse import FUSE, FuseOSError, Operations

from billabong import billabong
from billabong.settings import inventory, settings


def id_from_path(path):
    """Get the blob id from a FUSE path."""
    if path.startswith('/blobs/'):
        id_ = path[len('/blobs/'):]
    elif path.startswith('/files/'):
        filename = path.split('/')[-1]
        id_ = inventory.id_from_filename(filename)
    else:
        id_ = None

    if id_:
        return id_
    else:
        raise FuseOSError(errno.ENOENT)


class BillabongFilesystem(Operations):

    """Fuse file system on top of Billabong."""

    # ----- File methods -----

    def getattr(self, path, fh=None):
        """Hardcoded implementation of getattr."""
        if path in ('/', '/blobs', '/files'):
            return dict(
                st_mode=16877,
                st_ino=7077891,
                st_dev=64514,
                st_nlink=37,
                st_uid=1000,
                st_gid=1000,
                st_size=4096,
                st_atime=1428702934,
                st_mtime=1428702934,
                st_ctime=1428702934,
            )
        else:
            id_ = id_from_path(path)
            print('id_', path, id_)
            meta = inventory.get_record(id_)
            return dict(
                st_mode=33188,
                st_ino=7093655,
                st_dev=64514,
                st_nlink=1,
                st_uid=1000,
                st_gid=1000,
                st_size=meta['size'],
                st_atime=1428701319,
                st_mtime=1428514886,
                st_ctime=1428514886
            )

    def readdir(self, path, fh):
        """List directory content."""
        if path == '/':
            return ['blobs', 'files']
        elif path == '/blobs':
            return inventory.list_record_ids()
        elif path == '/files':
            return inventory.list_record_filenames()
        else:
            print('Unknown path', path)

    def read(self, path, length, offset, fh):
        """Read file data."""
        if path.startswith('/blobs/'):
            id_ = id_from_path(path)
            print(path, length, offset, fh)
            data = billabong.read(id_, offset=offset, length=length)
            return b''.join(data)
        elif path.startswith('/files/'):
            id_ = id_from_path(path)
            if id_:
                return b''.join(
                    billabong.read(id_, offset=offset, length=length))
            else:
                raise FuseOSError(errno.ENOENT)


def mount_fuse(path=None, foreground=True):
    """Mount the Billabong file system."""
    if path is None:
        path = settings['mount']

    FUSE(BillabongFilesystem(), path, foreground=foreground)
