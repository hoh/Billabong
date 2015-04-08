import sys
from diss import add_file
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

else:
    print('dis ls')
    print('dis add hello.txt')
