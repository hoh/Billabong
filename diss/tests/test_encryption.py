
from diss.encryption import copy_and_encrypt


def test_copy_and_encrypt():
    id_ = copy_and_encrypt('hello.txt', key=b'0'*32)
    assert id_ == ('d677661eee38488533213da47ab4e98f'
                   '9a6ed07f961ed53a2fd4d0dbfe06e5ee')
