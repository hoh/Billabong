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

"""Test CLI interface."""

import os

from .fixtures import record
assert record


def run(cmd):
    """Helper to test running a CLI command."""
    os.system('python -m billabong ' + cmd)


def test_cli(record):
    """Test main supported CLI commands."""
    ID = record['id']

    run('ls')
    run('records')
    run('blobs')
    run('info ' + ID)
    run('info ' + ID + ' --no-color')
    run('search txt')
    run('check')
    run('push')
    run('pull')
    run('echo ' + ID)
    run('status')
    run('version')

    run('add hello.txt')
