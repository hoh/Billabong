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


from shutil import copy2
from .settings import stores


def push_blobs():
    for store in stores[1:]:
        try:
            stores[0].push_to(store)
        except NotImplementedError:
            print("Push not implemented for '{}'".format(store))


def push_blob(blob_id, storage, remote):
    print('pushing blob', blob_id)
    path_local = stores[0]._blob_path(blob_id)
    path_remote = remote._blob_path(blob_id)
    copy2(path_local, path_remote)


def pull_blobs():
    for store in stores[1:]:
        try:
            store.push_to(stores[0])
        except NotImplementedError:
            print("Pull not implemented for '{}'".format(store))
