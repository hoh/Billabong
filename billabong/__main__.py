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


"""
# Billabong

A reliable, distributed, encrypted storage and backup solution for all of
your photos, videos, music and other static data.
"""

import os
import sys
from baker import command, run

try:
    from pygments import highlight
    from pygments.lexers import JsonLexer
    from pygments.formatters import TerminalFormatter
except ImportError:
    highlight = None

from billabong import billabong
from billabong.settings import inventory
from billabong.check import check_data, check_enc_data
from billabong.utils import dumps
from billabong.sync import push_blobs, pull_blobs


def print_record(record):
    if highlight and '--no-color' not in sys.argv:
        print(highlight(dumps(record),
                        JsonLexer(),
                        TerminalFormatter()))
    else:
        print(dumps(record))


@command
def ls():
    format_ = "{:>8} {:>8} {:>8}"
    for r in inventory.list_records():
        print(format_.format(r['id'][:8],
                             r['size'],
                             r['info']['filename']))


@command
def blobs():
    for i in inventory.list_record_ids():
        print(i)


@command
def add(*targets):
    for target in targets:
        record = billabong.add_file(target)
        print_record(record)


@command
def get(id_):
    raise NotImplemented


@command
def info(*ids):
    for id_ in ids:
        meta = inventory.get_record(id_)
        print_record(meta)


@command
def echo(id_):
    data = billabong.read(id_)

    # Write bytes to stdout:
    fp = os.fdopen(sys.stdout.fileno(), 'wb')
    for chunk in data:
        fp.write(chunk)
        fp.flush()


@command
def search(term):
    for i in inventory.search(term):
        print(i)


@command
def check():
    "Check the validity of all blobs and metadata"
    for i in inventory.list_record_ids():
        check_data(i)
        check_enc_data(i)


@command
def push():
    "Push blobs to sync storage"
    push_blobs()


@command
def pull():
    "Pull blobs from sync storage"
    pull_blobs()


@command
def status():
    "Print a global status of the inventory and storage."
    print("Inventory:")
    print("  {:>4} records".format(
          len(list(inventory.list_record_ids()))))
    print("  {:>4} bytes total".format(
          sum(i['size'] for i in inventory.list_records())))


@command
def mount(path=None, foreground=False):
    from billabong.fs import mount_fuse
    mount_fuse(path, foreground)


@command
def version():
    from billabong import __version__
    print(__version__)


if __name__ == '__main__':
    run()
