
from diss import list_blobs


def test_list_blobs():
    blobs = list(list_blobs())
    assert blobs == ['hello.txt']