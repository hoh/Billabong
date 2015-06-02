
# import json
from diss.settings import inventory
# from diss.utils import json_handler
from .testdata import ID


def test_get_meta():
    meta = inventory.get_record(ID)
    assert meta
