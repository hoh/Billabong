
from diss.encryption import random_key, copy_and_encrypt
from .testdata import ID


def test_random_key():
    key = random_key()
    assert len(key) == 32
    assert type(key) is bytes


def test_copy_and_encrypt():
    id_ = copy_and_encrypt('hello.txt', key=b'0'*32)
    assert id_ == ID
