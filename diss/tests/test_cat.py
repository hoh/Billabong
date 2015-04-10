
from diss import get_content
from .testdata import ID


def test_get_content():
    id_ = ID

    content = b"".join(get_content(id_))
    assert content == b"Hello world !\n\n"
