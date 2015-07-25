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

"""Tests Fuse filesystem."""

import pytest

from fuse import FuseOSError

from billabong.fs import id_from_path, BillabongFilesystem

from .fixtures import record
assert record


@pytest.fixture
def fusefs():
    """Fixture that creates a Fuse filesystem instance."""
    return BillabongFilesystem()


def test_id_from_path(record):
    """Test path resolver."""
    record_id = record['id']
    assert id_from_path('/blobs/SOMEID') == 'SOMEID'
    assert id_from_path('/files/hello.txt') == record_id

    with pytest.raises(FuseOSError):
        id_from_path('/DOES NOT EXIST')

    with pytest.raises(FuseOSError):
        id_from_path('/files/DOES NOT EXIST')


def test_readdir(record, fusefs):
    """Test directory listing."""
    record_id = record['id']
    assert fusefs.readdir('/', None) == ['blobs', 'files']
    assert set(fusefs.readdir('/blobs', None)).issuperset([record_id])
    assert set(fusefs.readdir('/files', None)).issuperset(['hello.txt'])
    assert fusefs.readdir('/does_not_exist', None) is None


def test_read(record, fusefs):
    """Test file reading."""
    record_id = record['id']
    data = fusefs.read('/blobs/' + record_id, 100, 0, None)
    assert data == b"Hello world !\n\n"

    data = fusefs.read('/files/hello.txt', 100, 0, None)
    assert data == b"Hello world !\n\n"

    with pytest.raises(FuseOSError):
        fusefs.read('/files/does_not_exist', 100, 0, None)


def test_getattr(record, fusefs):
    """Test getting file or directory attributes."""
    assert record
    assert fusefs.getattr('/').get('st_size')
    assert fusefs.getattr('/files/hello.txt').get('st_size')
