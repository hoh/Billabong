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


from billabong.settings import storage, remote_storages
from billabong.sync import push_blobs, push_blob

from .fixtures import record
assert record

remote = remote_storages[0]


def test_push_blobs():
    remote.delete_everything(confirm=True)
    push_blobs()
    remote.delete_everything(confirm=True)


def test_push_blob(record):
    ID = record['blob']
    remote.delete_everything(confirm=True)
    push_blob(ID, storage, remote)
    remote.delete_everything(confirm=True)
