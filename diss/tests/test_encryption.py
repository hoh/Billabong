
from diss.encryption import copy_and_encrypt
from .testdata import ID


def test_copy_and_encrypt():
    id_ = copy_and_encrypt('hello.txt', key=b'0'*32)
    assert id_ == ID
