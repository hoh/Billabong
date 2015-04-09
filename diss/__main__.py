import sys
from diss import add_file, get_meta
from diss.utils import dumps


if len(sys.argv) > 1:

    if sys.argv[1] in ('ls', 'list'):
        result = ('hello.txt', 'flower.png')
        for i in result:
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

    else:
        print('Unknown command')


else:
    print('dis ls')
    print('dis add hello.txt')
