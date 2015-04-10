
# import json
from diss.meta import get_meta
# from diss.utils import json_handler
from .testdata import ID


def test_get_meta():
    meta = get_meta(ID)
    assert meta
