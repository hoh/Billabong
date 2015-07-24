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


import pytest

from billabong.settings import inventory, storage
from billabong.core import Billabong


@pytest.fixture
def billabong():
    return Billabong(inventory, [storage])


@pytest.fixture
def record(billabong):
    filepath = "hello.txt"
    record = billabong.add_file(filepath=filepath)
    return record


def test_add(billabong):
    filepath = "hello.txt"
    record = billabong.add_file(filepath=filepath)
    assert record['info']['filename'] == filepath
    billabong.delete(record['id'])


def test_get(billabong, record):
    id_ = record['id']
    record_obtained = billabong.get(id_)
    for key in record.keys():
        assert record_obtained[key] == record[key]
    billabong.delete(record['id'])


def test_read(billabong, record):
    id_ = record['id']
    reader = billabong.read(id_)
    data = b''.join(reader)
    assert data == open("hello.txt", 'rb').read()
    billabong.delete(record['id'])
