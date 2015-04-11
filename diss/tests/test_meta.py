
from diss.meta import (list_ids,
                       list_paths,
                       list_filenames,
                       get_meta,
                       search_meta,
                       id_from_filename
                       )
from .testdata import ID


def test_list_ids():
    ids = list(list_ids())
    assert set(ids).issuperset([ID])


def test_list_paths():
    paths = list(list_paths())
    assert set(paths).issuperset(['hello.txt'])


def test_list_filenames():
    filenames = list(list_filenames())
    assert set(filenames).issuperset(['hello.txt'])


def test_get_meta():
    meta = get_meta(ID)
    expected = {
        'info': {'filename': 'hello.txt',
                 'mimetype': 'text/plain',
                 'path': 'hello.txt',
                 'type': 'ASCII text'},
        'size': 15,
    }
    for key in expected:
        assert meta[key] == expected[key]


def test_search_meta():
    ids = list(search_meta('hello'))
    assert set(ids).issuperset([ID])

    non_existing_ids = list(search_meta('DOES NOT EXIST'))
    assert non_existing_ids == []


def test_id_from_filename():
    id_ = id_from_filename('hello.txt')
    assert id_ == ID

    non_existing_id = id_from_filename('DOES NOT EXIST')
    assert non_existing_id is None
