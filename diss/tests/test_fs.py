
import pytest

from fuse import FuseOSError

from diss.fs import id_from_path, DissFilesystem
from .testdata import ID


@pytest.fixture
def fs():
    return DissFilesystem()


def test_id_from_path():
    assert id_from_path('/blobs/SOMEID') == 'SOMEID'
    assert id_from_path('/files/hello.txt') == ID

    with pytest.raises(FuseOSError):
        id_from_path('/DOES NOT EXIST')

    with pytest.raises(FuseOSError):
        id_from_path('/files/DOES NOT EXIST')


def test_readdir(fs):
    assert fs.readdir('/', None) == ['blobs', 'files']
    assert set(fs.readdir('/blobs', None)).issuperset([ID])
    assert set(fs.readdir('/files', None)).issuperset(['hello.txt'])
    assert fs.readdir('/does_not_exist', None) == None


def test_read(fs):
    data = fs.read('/blobs/' + ID, 100, 0, None)
    assert data == b"Hello world !\n\n"

    data = fs.read('/files/hello.txt', 100, 0, None)
    assert data == b"Hello world !\n\n"

    with pytest.raises(FuseOSError):
        fs.read('/files/does_not_exist', 100, 0, None)


def test_getattr(fs):
    assert fs.getattr('/').get('st_size')
    assert fs.getattr('/files/hello.txt').get('st_size')
