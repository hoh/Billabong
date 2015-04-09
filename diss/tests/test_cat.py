
from diss import get_content

ID = "d1477532aa7e401f3050280cdf86d6ea98a9c01f23d4c905aa0f641635a20bb7"


def test_get_content():
    id_ = ID

    content = get_content(id_)
    assert content == "Hello world !\n\n"
