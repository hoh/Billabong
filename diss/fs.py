"""
FUSE file system over the blob system.
"""

import errno

from fuse import FUSE, FuseOSError, Operations

from diss import get_content
from diss.meta import list_ids, list_filenames, get_meta, id_from_filename


def id_from_path(path):
    "Get the blob id from a FUSE path"
    if path.startswith('/blobs/'):
        id_ = path[len('/blobs/'):]
    elif path.startswith('/files/'):
        filename = path.split('/')[-1]
        id_ = id_from_filename(filename)
    else:
        id_ = None

    if id_:
        return id_
    else:
        raise FuseOSError(errno.ENOENT)


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
            id_ = id_from_path(path)
            print('id_', path, id_)
            meta = get_meta(id_)
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
        if path == '/':
            return ['blobs', 'files']
        elif path == '/blobs':
            return list_ids()
        elif path == '/files':
            return list_filenames()
        else:
            print('Unknown path', path)

    def read(self, path, length, offset, fh):
        if path.startswith('/blobs/'):
            id_ = id_from_path(path)
            print(path, length, offset, fh)
            data = get_content(id_)
            return b''.join(data)[offset:offset+length]
        elif path.startswith('/files/'):
            id_ = id_from_path(path)
            if id_:
                return b''.join(get_content(id_))[offset:offset+length]
            else:
                raise FuseOSError(errno.ENOENT)

if __name__ == '__main__':
    FUSE(DissFilesystem(), '/home/okso/diss', foreground=True)
