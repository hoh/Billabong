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

"""Test core Billabong classes."""


from .fixtures import billabong, record
assert record


def test_add_file_with_tags():
    tags = ['hello', 'world']
    record = billabong.add_file('hello.txt', key=b'0'*32, tags=tags)
    billabong.delete(record['id'])


def test_get(record):
    """Test getting a record from an id on Billabong object."""
    id_ = record['id']
    record_obtained = billabong.get(id_)
    for key in record.keys():
        assert record_obtained[key] == record[key]


def test_read(record):
    """Test getting cleartext data from an id on Billabong object."""
    id_ = record['id']
    reader = billabong.read(id_)
    data = b''.join(reader)
    assert data == open("hello.txt", 'rb').read()


def test_delete():
    """Test deleting a record and its blob from the inventory."""
    record = billabong.add_file('hello.txt')
    id_ = record['id']
    blob_id = record['blob']

    billabong.delete(id_)
    assert id_ not in billabong.inventory.list_record_ids()
    assert not billabong.stores[0].contains(blob_id)
