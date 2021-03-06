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
Billabong.

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
from billabong.settings import inventory, stores, settings, TMPSTORAGE_PATH
from billabong.check import check_data
from billabong.utils import dumps
from billabong.sync import push_blobs, pull_blobs
from billabong.archive import NotEncryptedZipArchive


def print_record(record):
    """Print a record with indentation and syntax highlighting if available."""
    if highlight and '--no-color' not in sys.argv:
        print(highlight(dumps(record),
                        JsonLexer(),
                        TerminalFormatter()))
    else:
        print(dumps(record))


@command
def ls(partial=True):
    """List short records ids with filename from the inventory."""
    format_ = "{:>8} {:>8} {:>8}"
    for record in inventory.list_records():
        id_ = record['id'][:8] if partial else record['id']
        print(format_.format(id_,
                             record['size'],
                             record['info']['filename']))


@command
def records():
    """List all records ids from the inventory."""
    for i in inventory.list_record_ids():
        print(i)


@command
def blobs():
    """List all blob ids from the first storage."""
    for i in stores[0].list_blob_ids():
        print(i)


@command
def tags():
    """List all tags from the inventory."""
    for i in inventory.list_record_tags():
        print(i)


@command
def add(tags='', *targets):
    """Import one or several files and print resulting records."""
    tags = tags.split(',') if tags else None
    for target in targets:
        record = billabong.add_file(target, tags=tags)
        print_record(record)


@command
def info(*ids):
    """Print record content from one or several record ids."""
    for id_ in ids:
        if len(id_) < 32:  # Allow use of short partial_id
            id_ = meta = inventory.search_id(partial_id=id_).__next__()
        meta = inventory.get_record(id_)
        print_record(meta)


@command
def echo(id_):
    """Print blob content to standard output for the given record id."""
    data = billabong.read(id_)

    # Write bytes to stdout:
    fdesc = os.fdopen(sys.stdout.fileno(), 'wb')
    for chunk in data:
        fdesc.write(chunk)
        fdesc.flush()


@command
def search(term):
    """Search for the given term and return id of records matching the term."""
    for i in inventory.search(term):
        print(i)


@command
def check():
    """Check the validity of all blobs and metadata."""
    for i in inventory.list_record_ids():
        check_data(i)


@command
def push():
    """Push blobs to sync storage."""
    push_blobs()


@command(name='stores')
def list_stores():
    """List remote stores."""
    for store in stores:
        print(store)


@command
def pull():
    """Pull blobs from sync storage."""
    pull_blobs()


@command
def archive(path):
    """Copy the inventory into a (encrypted) file."""
    archive = NotEncryptedZipArchive(path)
    archive.update(inventory)
    print("Saved archive as '{}'".format(path))


@command
def status():
    """Print a global status of the inventory and storage."""
    print("Inventory:")
    print("  {:>4} records"
          .format(len(list(inventory.list_record_ids()))))
    print("  {:>4} bytes total"
          .format(sum(i['size'] for i in inventory.list_records())))


@command
def mount(path=None, foreground=False):
    """Mount data as a filesystem."""
    from billabong.fs import mount_fuse
    mount_fuse(path, foreground)


@command
def version():
    """Print software version."""
    from billabong import __version__
    print(__version__)


@command
def config():
    """Print current configuration."""
    print("Inventory:")
    print("  -", inventory)
    print("Storages:")
    for store in stores:
        print("  -", store)
    print("Temporary storage:", TMPSTORAGE_PATH)
    print("FUSE mount path:", settings.get('mount'))

if __name__ == '__main__':
    run()
