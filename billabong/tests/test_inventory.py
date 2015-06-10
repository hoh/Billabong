
from billabong.settings import inventory

from .fixtures import record
assert record


def test_list_records(record):
    ID = record['id']
    ids = list(inventory.list_record_ids())
    assert set(ids).issuperset([ID])


def test_list_paths(record):
    paths = list(inventory.list_record_paths())
    assert set(paths).issuperset(['hello.txt'])


def test_list_filenames(record):
    filenames = list(inventory.list_record_filenames())
    assert set(filenames).issuperset(['hello.txt'])


def test_get_meta(record):
    ID = record['id']
    meta = inventory.get_record(ID)
    expected = {
        'info': {'filename': 'hello.txt',
                 'mimetype': 'text/plain',
                 'path': 'hello.txt',
                 'type': 'ASCII text'},
        'size': 15,
    }
    for key in expected:
        assert meta[key] == expected[key]


def test_search_meta(record):
    ID = record['id']
    ids = list(inventory.search('hello'))
    assert set(ids).issuperset([ID])

    non_existing_ids = list(inventory.search('DOES NOT EXIST'))
    assert non_existing_ids == []


def test_id_from_filename(record):
    ID = record['id']
    id_ = inventory.id_from_filename('hello.txt')
    assert id_ == ID

    non_existing_id = inventory.id_from_filename('DOES NOT EXIST')
    assert non_existing_id is None


def test_delete_everything():
    inventory.delete_everything(confirm=True)


def test_search_id(record):
    ID = record['id']
    inventory.search_id(ID[:10])
