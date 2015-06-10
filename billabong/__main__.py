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

from diss import add_file, get_content
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
def add(target):
    record = add_file(target)
    print_record(record)


@command
def get(id_):
    raise NotImplemented


@command
def info(id_):
    meta = inventory.get_record(id_)

    if highlight and '--no-color' not in sys.argv:
        print(highlight(dumps(meta),
                        JsonLexer(),
                        TerminalFormatter()))
    else:
        print(dumps(meta))


@command
def echo(id_):
    data = get_content(id_)

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

if __name__ == '__main__':
    run()
