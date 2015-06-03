
import os
from .testdata import ID


def run(cmd):
    print('python -m diss ' + cmd)
    os.system('python -m diss ' + cmd)


def test_cli():
    run('ls')
    run('info ' + ID)
    run('search txt')
