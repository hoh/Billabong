
from billabong.settings import inventory

from .fixtures import record
assert record


def test_get_meta(record):
    id_ = record['id']
    meta = inventory.get_record(id_)
    assert meta
