
from diss.encryption import copy_and_encrypt


def test_copy_and_encrypt():
    id_ = copy_and_encrypt('hello.txt', key='SOMEKEY')
    assert id_ == 'ENC_HASH_1234567890'
