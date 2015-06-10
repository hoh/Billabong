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


import json

from .storage import load_storage
from .inventory import load_inventory


def load_settings(path):
    return json.load(open(path))

TMPSTORAGE_PATH = './data/tmp'

settings = load_settings('billabong/settings.json')

inventory = load_inventory(settings['inventory'])
storage = load_storage(settings['storage'])


remote_storages = [load_storage(r)
                   for r in settings.get('storages', ())]
