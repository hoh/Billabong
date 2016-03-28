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

"""Test file import into Billabong."""

import pytest

import json
from datetime import datetime
from billabong import billabong
from billabong.utils import json_handler

from billabong.settings import inventory, stores

STORE = stores[0]
HASH = "fc7d4f43945d94c874415e3bd9a6e181f8c84f8a36f586389405e391c01e48b2"


def test_add_file():
    """Test adding a file with a defined key."""
    # Test using a know replicable :key:
    meta = billabong.add_file('hello.txt', key=b'0'*32)
    assert meta

    assert meta['hash'].startswith('sha256-')
    assert meta['hash'] == 'sha256-' + HASH

    assert meta['info']['path']
    assert meta['info']['filename']

    assert meta['timestamp'] > 1450000000
    assert isinstance(meta['datetime'], datetime)

    inventory.delete(meta['id'])
    STORE.delete(meta['blob'])


def test_add_random_key():
    """Test adding a file with no defined key."""
    meta = billabong.add_file('lorem.txt')
    assert meta
    inventory.delete(meta['id'])
    STORE.delete(meta['blob'])


def test_add_file_not_found():
    """Test that adding a file that does not exist fails."""
    with pytest.raises(FileNotFoundError):
        billabong.add_file('does not exist.txt')


def test_add_file_json():
    """Test that the a record can is JSON serializable."""
    meta = billabong.add_file('hello.txt', key=b'0'*32)
    assert len(json.dumps(meta, default=json_handler)) > 1  # JSON serializable
    inventory.delete(meta['id'])
    STORE.delete(meta['blob'])
