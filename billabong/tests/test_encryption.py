# Copyright (c) 2015 "Hugo Herter http://hugoherter.com"
#
# This file is part of Billabong.
#
# Intercom is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Tests encryption functions."""

from billabong.settings import stores
from billabong.encryption import random_key, copy_and_encrypt, decrypt_blob

from .fixtures import record
assert record

store = stores[0]


def test_random_key():
    """Test generating a random key."""
    key = random_key()
    assert len(key) == 32
    assert type(key) is bytes


def test_copy_and_encrypt(record):
    """Test file encryption."""
    blob_id_ = copy_and_encrypt(store, 'hello.txt', key=b'0'*32)
    assert blob_id_ == record['blob']


def test_decrypt_blob(record):
    """Test file decryption."""
    blob_id = record['blob']
    g = decrypt_blob(store, blob_id, b'0'*32)
    data = b''.join(g)
    assert data == b'Hello world !\n\n'


def test_decrypt_offset():
    """Test partial file decryption."""
    offset = 340
    length = 69
    expected = open('lorem.txt', 'rb').read()[offset:offset+length]
    assert expected == (b"Qui animated corpse, cricket bat max brucks "
                        b"terribilem incessu zomby.")

    id_ = copy_and_encrypt(store, 'lorem.txt', key=b'0'*32)

    g = decrypt_blob(store, id_, b'0'*32, offset=offset, length=length)

    data = b''.join(g)
    assert data == expected
