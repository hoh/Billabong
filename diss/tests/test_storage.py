
from diss import add_file
from diss.storage import list_blobs


def test_list_blobs():
    meta = add_file('hello.txt', key=b'0'*32)
    assert meta
    blobs = list_blobs()
    assert blobs
