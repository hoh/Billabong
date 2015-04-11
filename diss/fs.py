"""
FUSE file system over the blob system.
"""

import os
import sys
import errno
import mmap  # temporary replacement for file access

from fuse import FUSE, FuseOSError, Operations

from diss import get_content
from diss.meta import list_ids, list_filenames, get_meta, meta_by_filename
from diss.settings import STORAGE_PATH, METADATA_PATH


class DissFilesystem(Operations):

    def __init__(self):
        pass

    # ----- File methods -----

    def getattr(self, path, fh=None):
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
            return dict(
                st_mode=33188,
                st_ino=7093655,
                st_dev=64514,
                st_nlink=1,
                st_uid=1000,
                st_gid=1000,
                st_size=378,
                st_atime=1428701319,
                st_mtime=1428514886,
                st_ctime=1428514886
            )

    def readdir(self, path, fh):
        if path == '/':
            return ['blobs', 'files']
        elif path == '/blobs':
            return list_ids()
        elif path == '/files':
            return list_filenames()
        else:
            print('Unknown path', path)

    def read(self, path, length, offset, fh):
        print('read', path)
        if path.startswith('/blobs/'):
            id_ = path[1:]  # Strip heading /
            print(path, length, offset, fh)
            data = get_content(id_)
            return b''.join(data)
        elif path.startswith('/files/'):
            filename = path[len('/files/'):]
            print('filename', [filename])
            id_ = meta_by_filename(filename)
            print('id_', id_)
            if id_:
                return b''.join(get_content(id_))[:length]
            else:
                raise FuseOSError(errno.ENOENT)

if __name__ == '__main__':
    FUSE(DissFilesystem(), '/home/okso/diss', foreground=True)
