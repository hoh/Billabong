
import os.path

from .settings import METADATA_PATH
from .utils import loads, dumps


def list_blobs():
    for id_ in os.listdir(METADATA_PATH):
        id_ = id_.replace('.json', '')
        meta = get_meta(id_)
        yield meta['info']['path']


def get_meta(id_):
    "Load metadata for the given id."
    filepath = os.path.join(METADATA_PATH, id_ + '.json')
    return loads(open(filepath, 'r').read())


def search_meta(term):
    "Search for a term in the metadata and return the corresponding ids"
    for id_ in os.listdir(METADATA_PATH):
        id_ = id_.replace('.json', '')
        meta = get_meta(id_)
        if term in dumps(meta):
            yield id_
