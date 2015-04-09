
# import json
from diss import get_meta
# from diss.utils import json_handler

ID = "d1477532aa7e401f3050280cdf86d6ea98a9c01f23d4c905aa0f641635a20bb7"


def test_get_meta():
    meta = get_meta(ID)
    assert meta
