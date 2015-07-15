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


"""Blob Storage."""

from .abstract import Storage
from .folder import FolderStorage
from .http import HTTPStorage
from .ssh import SSHStorage

assert Storage
assert FolderStorage
assert HTTPStorage
assert SSHStorage


def load_storage(settings):
    """Instanciate a storage instance from settings."""
    type_ = settings['type']
    args = settings.get('args', {})

    if type_ == 'FolderStorage':
        return FolderStorage(**args)
    elif type_ == 'HTTPStorage':
        return HTTPStorage(**args)
    elif type_ == 'SSHStorage':
        return SSHStorage(**args)
    else:
        raise ValueError("Unknown type", type_)
