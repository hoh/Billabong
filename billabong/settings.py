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

"""Load settings and initialize inventory and stores."""

import os
import json

from .storage import load_store
from .inventory import load_inventory

settings_path_candidates = [
    "./billabong.json",
    os.path.expanduser("~/.config/billabong.json"),
    "/etc/billabong.json",
]

for candidate in settings_path_candidates:
    if os.path.isfile(candidate):
        settings_path = candidate
        break
else:
    raise FileNotFoundError("Billabong configuration file not found.")

settings = json.load(open(settings_path))

TMPSTORAGE_PATH = settings.get('tmp_directory', '/tmp')

inventory = load_inventory(settings['inventory'])
stores = [load_store(r) for r in settings['stores']]
