
import json
from diss import add_file
from diss.utils import json_handler


def test_add_file():
    expected_hash = ('fc7d4f43945d94c874415e3bd9a6e181f'
                     '8c84f8a36f586389405e391c01e48b2')

    meta = add_file('hello.txt')
    assert meta

    assert meta['hash'].startswith('sha256-')
    assert meta['hash'] == 'sha256-' + expected_hash

    assert meta['path']['relative']
    assert meta['path']['absolute']
    assert meta['path']['filename']


def test_add_file_json():
    meta = add_file('hello.txt')
    assert len(json.dumps(meta, default=json_handler)) > 1  # JSON serializable
