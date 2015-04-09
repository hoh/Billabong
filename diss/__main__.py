import sys
from diss import add_file, get_meta, list_blobs, get_content
from diss.utils import dumps

HELP = '''DIstributed Storage System

dis ls
dis add somefile.png
dis get $HASH
dis info $HASH
dis echo $HASH
'''

if len(sys.argv) > 1:

    if sys.argv[1] in ('ls', 'list'):
        for i in list_blobs():
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
        print(dumps(meta))

    elif sys.argv[1] == 'echo':
        id_ = sys.argv[2]
        data = get_content(id_)
        print(data)

    else:
        print('Unknown command')


else:
    print(HELP)
