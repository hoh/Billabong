
import json
from datetime import datetime
from diss.utils import json_handler


def test_encode_datetime():
    dico = {'date': datetime(2015, 4, 8)}
    assert json.dumps(dico, default=json_handler) \
        == '{"date": "2015-04-08T00:00:00"}'


def test_encode_datetime_subdico():
    dico = {'date': {'good': True, 'time': datetime(2015, 4, 8)}}
    encoded = json.dumps(dico, default=json_handler)
    assert '"time": "2015-04-08T00:00:00"' in encoded
