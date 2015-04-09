
import json
from diss import add_file
from diss.utils import json_handler

HASH = "fc7d4f43945d94c874415e3bd9a6e181f8c84f8a36f586389405e391c01e48b2"


def test_add_file():
    meta = add_file('hello.txt')
    assert meta

    assert meta['hash'].startswith('sha256-')
    assert meta['hash'] == 'sha256-' + HASH

    assert meta['info']['path']
    assert meta['info']['filename']


def test_add_file_json():
    meta = add_file('hello.txt')
    assert len(json.dumps(meta, default=json_handler)) > 1  # JSON serializable
