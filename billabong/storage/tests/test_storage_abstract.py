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


import pytest
from billabong.storage.abstract import Storage


def test_not_implemented():
    s = Storage()

    with pytest.raises(NotImplementedError):
        s.list_blob_ids()

    with pytest.raises(NotImplementedError):
        s.delete(id_='SOMEID')

    with pytest.raises(NotImplementedError):
        s.delete_everything(confirm=True)

    with pytest.raises(NotImplementedError):
        s.import_blob(id_='SOMEID', filename='/tmp/filename')

    with pytest.raises(NotImplementedError):
        s.read_in_chunks(id_='SOMEID', chunk_size=1024)

    with pytest.raises(NotImplementedError):
        s.missing_from(other_storage=Storage())

    with pytest.raises(NotImplementedError):
        s.push_to(other_storage=Storage())

    with pytest.raises(NotImplementedError):
        s.push_blob_to(id_='SOMEID', other_storage=Storage())
