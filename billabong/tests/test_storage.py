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


from billabong import billabong
from billabong.settings import inventory, stores

store = stores[0]


def test_list_blobs():
    meta = billabong.add_file('hello.txt', key=b'0'*32)
    assert meta
    blobs = list(store.list_blob_ids())
    assert blobs
    assert len(blobs) > 1

    inventory.delete(meta['id'])
    store.delete(meta['blob'])
