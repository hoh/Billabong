
import pytest

import json
from diss import add_file
from diss.utils import json_handler

from diss.settings import inventory, storage


HASH = "fc7d4f43945d94c874415e3bd9a6e181f8c84f8a36f586389405e391c01e48b2"


def test_add_file():
    # Test using a know replicable :key:
    meta = add_file('hello.txt', key=b'0'*32)
    assert meta

    assert meta['hash'].startswith('sha256-')
    assert meta['hash'] == 'sha256-' + HASH

    assert meta['info']['path']
    assert meta['info']['filename']

    inventory.delete(meta['id'])
    storage.delete(meta['blob'])


def test_add_random_key():
    meta = add_file('lorem.txt')
    assert meta
    inventory.delete(meta['id'])
    storage.delete(meta['blob'])


def test_add_file_not_found():
    with pytest.raises(FileNotFoundError):
        add_file('does not exist.txt')


def test_add_file_json():
    meta = add_file('hello.txt', key=b'0'*32)
    assert len(json.dumps(meta, default=json_handler)) > 1  # JSON serializable
    inventory.delete(meta['id'])
    storage.delete(meta['blob'])
