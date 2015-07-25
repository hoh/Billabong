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
