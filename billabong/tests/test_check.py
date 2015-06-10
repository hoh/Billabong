
from billabong.check import check_data

from .fixtures import record
assert record


def test_check_data(record):
    ID = record['id']
    check_data(id=ID)
