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

"""Test inventory methods."""

from billabong.settings import inventory

from .fixtures import record
assert record


def test_list_records(record):
    """Test listing record ids."""
    record_id = record['id']
    ids = list(inventory.list_record_ids())
    assert set(ids).issuperset([record_id])


def test_list_paths(record):
    """Test listing record paths."""
    assert record
    paths = list(inventory.list_record_paths())
    assert set(paths).issuperset(['hello.txt'])


def test_list_filenames(record):
    """Test listing record filenames."""
    assert record
    filenames = list(inventory.list_record_filenames())
    assert set(filenames).issuperset(['hello.txt'])


def test_list_tags(record):
    """Test listing record tags."""
    assert record['info']['tags'] == ['hello', 'ipsum']


def test_get_meta(record):
    """Test getting a record from the inventory."""
    record_id = record['id']
    meta = inventory.get_record(record_id)
    expected = {
        'info': {'filename': 'hello.txt',
                 'mimetype': 'text/plain',
                 'path': 'hello.txt',
                 'type': 'ASCII text',
                 'tags': ['hello', 'ipsum']},
        'size': 15,
    }
    for key in expected:
        assert meta[key] == expected[key]


def test_search_meta(record):
    """Test searching for data in the records."""
    record_id = record['id']
    ids = list(inventory.search('hello'))
    assert set(ids).issuperset([record_id])

    non_existing_ids = list(inventory.search('DOES NOT EXIST'))
    assert non_existing_ids == []


def test_id_from_filename(record):
    """Test getting a record id from its filename."""
    record_id = record['id']
    id_ = inventory.id_from_filename('hello.txt')
    assert id_ == record_id

    non_existing_id = inventory.id_from_filename('DOES NOT EXIST')
    assert non_existing_id is None


def test_delete_everything():
    """Test deleting every record in the inventory."""
    inventory.delete_everything()


def test_search_id(record):
    """Test searching records based on their id prefix."""
    record_id = record['id']
    inventory.search_id(record_id[:10])
