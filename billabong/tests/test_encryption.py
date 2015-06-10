
from billabong.encryption import random_key, copy_and_encrypt, decrypt_blob

from .fixtures import record
assert record


def test_random_key():
    key = random_key()
    assert len(key) == 32
    assert type(key) is bytes


def test_copy_and_encrypt(record):
    blob_id_ = copy_and_encrypt('hello.txt', key=b'0'*32)
    assert blob_id_ == record['blob']


def test_decrypt_blob(record):
    blob_id = record['blob']
    g = decrypt_blob(blob_id, b'0'*32)
    data = b''.join(g)
    assert data == b'Hello world !\n\n'


def test_decrypt_offset():
    offset = 340
    length = 69
    expected = open('lorem.txt', 'rb').read()[offset:offset+length]
    assert expected == (b"Qui animated corpse, cricket bat max brucks "
                        b"terribilem incessu zomby.")

    id_ = copy_and_encrypt('lorem.txt', key=b'0'*32)

    g = decrypt_blob(id_, b'0'*32, offset=offset, length=length)

    data = b''.join(g)
    assert data == expected
