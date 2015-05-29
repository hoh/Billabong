import os
import sys

try:
    from pygments import highlight
    from pygments.lexers import JsonLexer
    from pygments.formatters import TerminalFormatter
except ImportError:
    highlight = None

from diss import add_file, get_content
from diss.meta import list_ids, get_meta, search_meta
from diss.check import check_data
from diss.utils import dumps

HELP = '''DIstributed Storage System

dis ls
dis add $SOMEFILE
dis get $HASH
dis info $HASH
dis echo $HASH
dis search $TERM
dis check
'''

if len(sys.argv) > 1:

    if sys.argv[1] in ('ls', 'list'):
        for i in list_ids():
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
        meta = get_meta(id_)

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
        for i in search_meta(term):
            print(i)

    elif sys.argv[1] == 'check':
        # Check the validity of all blobs and metadata
        for i in list_ids():
            check_data(i)
    else:
        print('Unknown command')


else:
    print(HELP)
