import os
import sys

try:
    from pygments import highlight
    from pygments.lexers import JsonLexer
    from pygments.formatters import TerminalFormatter
except ImportError:
    highlight = None

from diss import add_file, get_content
from diss.settings import inventory
from diss.check import check_data, check_enc_data
from diss.utils import dumps
from diss.sync import push_blobs

HELP = '''DIstributed Storage System

dis ls
dis lsblobs
dis add $SOMEFILE
dis get $HASH
dis info $HASH
dis echo $HASH
dis search $TERM
dis check
'''

if len(sys.argv) > 1:

    if sys.argv[1] in ('ls', 'list'):
        format_ = "{:>8} {:>8} {:>8}"
        for r in inventory.list_records():
            print(format_.format(r['id'][:8],
                                 r['size'],
                                 r['info']['filename']))

    elif sys.argv[1] == 'lsblobs':
        for i in inventory.list_record_ids():
            print(i)

    elif sys.argv[1] == 'add':
        target = sys.argv[2]
        meta = add_file(target)
        print(dumps(meta))

    elif sys.argv[1] == 'get':
        target = sys.argv[2]
        raise NotImplemented

    elif sys.argv[1] == 'info':
        id_ = sys.argv[2]
        meta = inventory.get_record(id_)

        if highlight and '--no-color' not in sys.argv:
            print(highlight(dumps(meta),
                            JsonLexer(),
                            TerminalFormatter()))
        else:
            print(dumps(meta))

    elif sys.argv[1] == 'echo':
        id_ = sys.argv[2]
        data = get_content(id_)

        # Write bytes to stdout:
        fp = os.fdopen(sys.stdout.fileno(), 'wb')
        for chunk in data:
            fp.write(chunk)
            fp.flush()

    elif sys.argv[1] == 'search':
        term = sys.argv[2]
        for i in inventory.search(term):
            print(i)

    elif sys.argv[1] == 'check':
        # Check the validity of all blobs and metadata
        for i in inventory.list_record_ids():
            check_data(i)
            check_enc_data(i)

    elif sys.argv[1] == 'push':
        # Push blobs to sync storage
        push_blobs()
    else:
        print('Unknown command')


else:
    print(HELP)
