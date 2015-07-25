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

"""Utility pure functions for handling JSON and reading files."""

import datetime
import json


def json_handler(obj):
    """Convert datetime objects to string when dumping JSON."""
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return obj.decode()
    else:
        print([obj])
        return json.JSONEncoder().default(obj)


def dumps(obj, indent=2):
    """Dump an object to JSON while handling datetime objects conversion."""
    return json.dumps(obj, default=json_handler, indent=indent)


def json_loader(dico):
    """Convert strings to datetime objects when loading JSON."""
    for key, value in dico.items():
        if key == 'timestamp' and isinstance(value, str):
            try:
                dico[key] = datetime.datetime.strptime(value,
                                                       "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError as error:
                print("WARNING: ", error)
    return dico


def loads(string):
    """Load JSON while handling datetime objects conversion."""
    return json.loads(string, object_hook=json_loader)


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.

    Default chunk size: 1KiB (1024 bytes).
    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
