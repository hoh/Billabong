
import os
import os.path

from .settings import METADATA_PATH
from .utils import loads, dumps


def list_records():
    "List all ids present in the metadata."
    for id_ in os.listdir(METADATA_PATH):
        yield id_.replace('.json', '')


def list_paths():
    "List all blobs by their path."
    for id_ in list_records():
        meta = get_meta(id_)
        yield meta['info']['path']


def list_filenames():
    "List all blobs by their filename."
    for id_ in list_records():
        meta = get_meta(id_)
        yield meta['info']['filename'].replace('/', '.')


def get_meta(id_):
    "Load metadata for the given id."
    filepath = os.path.join(METADATA_PATH, id_ + '.json')
    return loads(open(filepath, 'r').read())


def search_meta(term):
    "Search for a term in the metadata and return the corresponding ids"
    for id_ in list_records():
        meta = get_meta(id_)
        if term in dumps(meta):
            yield id_


def id_from_filename(filename):
    "Return the id of the first document matching filename"
    for id_ in list_records():
        meta = get_meta(id_)
        if filename == meta['info']['filename']:
            return id_


def delete_record(id_):
    "Delete a record"
    os.remove(os.path.join(METADATA_PATH, id_ + '.json'))
