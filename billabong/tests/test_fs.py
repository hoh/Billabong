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
def fs():
    """Fixture that creates a Fuse filesystem instance."""
    return BillabongFilesystem()


def test_id_from_path(record):
    """Test path resolver."""
    ID = record['id']
    assert id_from_path('/blobs/SOMEID') == 'SOMEID'
    assert id_from_path('/files/hello.txt') == ID

    with pytest.raises(FuseOSError):
        id_from_path('/DOES NOT EXIST')

    with pytest.raises(FuseOSError):
        id_from_path('/files/DOES NOT EXIST')


def test_readdir(record, fs):
    """Test directory listing."""
    ID = record['id']
    assert fs.readdir('/', None) == ['blobs', 'files']
    assert set(fs.readdir('/blobs', None)).issuperset([ID])
    assert set(fs.readdir('/files', None)).issuperset(['hello.txt'])
    assert fs.readdir('/does_not_exist', None) is None


def test_read(record, fs):
    """Test file reading."""
    ID = record['id']
    data = fs.read('/blobs/' + ID, 100, 0, None)
    assert data == b"Hello world !\n\n"

    data = fs.read('/files/hello.txt', 100, 0, None)
    assert data == b"Hello world !\n\n"

    with pytest.raises(FuseOSError):
        fs.read('/files/does_not_exist', 100, 0, None)


def test_getattr(record, fs):
    """Test getting file or directory attributes."""
    assert fs.getattr('/').get('st_size')
    assert fs.getattr('/files/hello.txt').get('st_size')
