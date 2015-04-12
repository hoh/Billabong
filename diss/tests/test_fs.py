
import os
import pytest

from fuse import FUSE, FuseOSError

from diss.fs import id_from_path, DissFilesystem
from .testdata import ID


def test_id_from_path():
    assert id_from_path('/blobs/SOMEID') == 'SOMEID'
    assert id_from_path('/files/hello.txt') == ID

    with pytest.raises(FuseOSError):
        id_from_path('/DOES NOT EXIST')

    with pytest.raises(FuseOSError):
        id_from_path('/files/DOES NOT EXIST')


def test_DissFilesystem():
    mount_path = 'mount_dissfs'
    if not os.path.isdir(mount_path):
        os.mkdir(mount_path)
    fs = DissFilesystem()
    print(fs)
    assert fs.readdir('/', 0) == ['blobs', 'files']

    data = fs.read('/files/hello.txt', 100, 0, None)
    assert data == b"Hello world !\n\n"
