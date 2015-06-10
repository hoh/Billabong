
import json

from .storage import load_storage
from .inventory import load_inventory


def load_settings(path):
    return json.load(open(path))

TMPSTORAGE_PATH = './tmpdata'

settings = load_settings('diss/settings.json')

inventory = load_inventory(settings['inventory'])
storage = load_storage(settings['storage'])


remote_storages = [load_storage(r)
                   for r in settings.get('storages', ())]
