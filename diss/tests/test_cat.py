
from diss import get_content
from .testdata import ID


def test_get_content():
    id_ = ID

    content = get_content(id_)
    assert content == "Hello world !\n\n"
