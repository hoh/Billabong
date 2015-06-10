
from billabong import get_content

from .fixtures import record
assert record


def test_get_content(record):
    ID = record['id']

    content = b"".join(get_content(ID))
    assert content == b"Hello world !\n\n"
