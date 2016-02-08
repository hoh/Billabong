# Copyright (c) 2016 "Hugo Herter http://hugoherter.com"
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

"""Test archive classes."""

import os.path
import pytest
from zipfile import is_zipfile, ZipFile

from billabong.settings import inventory
from billabong.archive import Archive, NotEncryptedZipArchive

from .fixtures import record
assert record


def test_abstract_archive():
    archive = Archive(path='/tmp/archive')
    with pytest.raises(NotImplementedError):
        archive.update(inventory)


def test_NotEncryptedZipArchive(record):
    PATH = '/tmp/test_archive_path.zip'
    print(record['id'])
    archive = NotEncryptedZipArchive(PATH)
    archive.update(inventory)
    assert os.path.isfile(PATH)
    assert is_zipfile(PATH)
    with ZipFile(PATH) as zipfile:
        assert "{}.json".format(record['id']) in zipfile.namelist()
