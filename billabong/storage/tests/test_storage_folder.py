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

"""Test folder storage implementation."""

import os
import pytest
from billabong.storage.folder import FolderStorage


@pytest.fixture
def storage():
    """Fixture that creates a folder storage instance."""
    path = '/tmp/test_storage'
    if not os.path.isdir(path):
        os.mkdir(path)
    return FolderStorage(path=path)


def test__init(storage):
    """Test the storage has been initialized correctly."""
    assert storage
    assert storage.path


def test_blob_path(storage):
    """Test internal blob_path method."""
    expected_path = storage.path + '/SOMEID'
    assert storage._blob_path(id_='SOMEID') == expected_path


def test_repr(storage):
    """Test the string representation of the storage."""
    assert str(storage) == 'Folder: /tmp/test_storage'
