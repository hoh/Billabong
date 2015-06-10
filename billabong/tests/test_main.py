
import os

from .fixtures import record
assert record


def run(cmd):
    os.system('python -m billabong ' + cmd)


def test_cli(record):
    ID = record['id']

    run('ls')
    run('blobs')
    run('info ' + ID)
    run('search txt')
    run('check')
    run('push')
    run('pull')
    run('echo ' + ID)
