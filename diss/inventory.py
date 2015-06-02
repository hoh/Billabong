"""
Storage and manipulation of records containing metadata.
"""
import os
import os.path

from .utils import loads, dumps


class Inventory:
    """An Inventory represents a location where records of metadata can be stored
    and synced from/to.
    """

    def list_record_ids(self):
        raise NotImplementedError

    def delete(self, id_):
        raise NotImplementedError

    def get_record(self, id_):
        raise NotImplementedError

    def save_record(self, value):
        raise NotImplementedError

    def list_records(self):
        "Yield all records content."
        for id_ in self.list_record_ids():
            yield self.get_record(id_)

    def delete_everything(self, *, confirm=False):
        "Delete every record from the inventory"
        for record_id in self.list_record_ids():
            self.delete(record_id)

    def list_record_keyvalues(self, key):
        "List the value of one key for all records."
        for id_ in self.list_record_ids():
            record = self.get_record(id_)
            yield record['info'][key]

    def list_record_paths(self):
        "List all the paths of all records, used for 'ls' for example."
        yield from self.list_record_keyvalues('path')

    def list_record_filenames(self):
        "List all records by their filename, used for 'ls' for example."
        for value in self.list_record_keyvalues('filename'):
            yield value.replace('/', '.')

    def search(self, term):
        "Search for a term in the metadata and return the corresponding ids"
        for record in self.list_records():
            if term in dumps(record):
                yield record['id']

    def id_from_filename(self, filename):
        "Return the id of the first record matching filename"
        for record in self.list_records():
            if filename == record['info']['filename']:
                return record['id']


class FolderInventory(Inventory):
    """Inventory in a folder accessible via the local filesystem.
    """

    def __init__(self, path):
        self.path = path

    def _record_path(self, id_):
        "Returns the path on the filesystem where a record is stored."
        return os.path.join(self.path, id_ + '.json')

    def list_record_ids(self):
        "List all record ids present in the inventory."
        for filename in os.listdir(self.path):
            id_ = filename[:-len('.json')]
            yield id_

    def delete(self, id_):
        "Delete a record from the inventory"
        os.remove(self._record_path(id_))

    def get_record(self, id_):
        "Load metadata for the given id."
        filepath = self._record_path(id_)
        return loads(open(filepath, 'r').read())

    def save_record(self, record):
        destination = self._record_path(record['id'])
        open(destination, 'w').write(dumps(record))
