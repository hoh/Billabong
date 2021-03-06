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

"""Fixtures used in tests."""

import pytest
from billabong import billabong
from billabong.settings import inventory, stores


@pytest.fixture
def record(request):
    """Import a file, return the record and delete them after the test."""
    new_record = billabong.add_file('hello.txt', tags=['hello', 'ipsum'],
                                    key=b'0'*32)

    def fin():
        """Delete created record and blob at the end of the test."""
        inventory.delete(new_record['id'])
        for store in stores:
            try:
                store.delete(new_record['blob'])
            except (NotImplementedError, FileNotFoundError):
                pass
    request.addfinalizer(fin)
    return new_record
