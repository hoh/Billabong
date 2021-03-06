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

"""Test validation of data integrity."""

import pytest
from billabong.check import check_data

from .fixtures import record
assert record


def test_check_data(record):
    """Test validation of data integrity using 'check_data'."""
    check_data(id_=record['id'])
    check_data(record=record)

    with pytest.raises(ValueError):
        check_data()


def check_enc_data(record):
    """Test validation of encrypted data checksums."""
    blob_id = record['blob']
    check_enc_data(blob_id)
