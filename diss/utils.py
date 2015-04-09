
import datetime
import json


def json_handler(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return obj.decode()
    else:
        print([obj])
        return json.JSONEncoder().default(obj)


def dumps(obj, indent=2):
    return json.dumps(obj, default=json_handler, indent=indent)


loads = json.loads


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
