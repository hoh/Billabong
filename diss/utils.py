
import datetime
import json


def json_handler(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    else:
        return json.JSONEncoder().default(obj)


def dumps(obj, indent=2):
    return json.dumps(obj, default=json_handler, indent=indent)
