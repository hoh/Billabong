
from diss.encryption import copy_and_encrypt


def test_copy_and_encrypt():
    id_ = copy_and_encrypt('hello.txt', key=b'0'*32)
    assert id_ == 'ENC_HASH_1234567890'
