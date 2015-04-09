
from diss import get_content


def test_get_content():
    id_ = ('0c3d74c6f31399bac7f85312c63393a3'
           '2034f94b94b24d4f15309fb498b8f5c3')

    content = get_content(id_)
    assert content == "Hello world !\n\n"
