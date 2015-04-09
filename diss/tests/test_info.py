
# import json
from diss import get_meta
# from diss.utils import json_handler


def test_get_meta():
    meta = get_meta('0c3d74c6f31399bac7f85312c63393a3'
                    '2034f94b94b24d4f15309fb498b8f5c3')
    assert meta
