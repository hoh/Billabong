# Copyright (c) 2015 "Hugo Herter http://hugoherter.com"
#
# This file is part of Billabong.
#
# Intercom is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""Storage and manipulation of records containing metadata."""

import os
import os.path

from .utils import loads, dumps


class Inventory:

    """Location where records of metadata can be stored and synced from/to."""

    def list_record_ids(self):
        """List all records ids."""
        raise NotImplementedError

    def delete(self, id_):
        """Delete the record corresponding to the given id."""
        raise NotImplementedError

    def get_record(self, id_):
        """Return records data from a record id."""
        raise NotImplementedError

    def save_record(self, value):
        """Save a new record in the inventory."""
        raise NotImplementedError

    def list_records(self):
        """Yield all records content."""
        for id_ in self.list_record_ids():
            yield self.get_record(id_)

    def delete_everything(self):
        """Delete every record from the inventory."""
        for record_id in self.list_record_ids():
            self.delete(record_id)

    def list_record_keyvalues(self, key):
        """List the value of one key for all records."""
        for id_ in self.list_record_ids():
            record = self.get_record(id_)
            yield record['info'][key]

    def list_record_tags(self):
        """List the set of distinct tags present in all records."""
        yielded = set()
        for record in self.list_records():
            tags = set(record['info'].get('tags', []))
            for tag in tags - yielded:
                yield tag
            yielded.update(tags)

    def list_record_paths(self):
        """List all the paths of all records, used for 'ls' for example."""
        yield from self.list_record_keyvalues('path')

    def list_record_filenames(self):
        """List all records by their filename, used for 'ls' for example."""
        for value in self.list_record_keyvalues('filename'):
            yield value.replace('/', '.')

    def list_records_with_tag(self, tag):
        """List all records tagged with the given tag."""
        for record in self.list_records():
            if tag in record['info'].get('tags', []):
                yield record

    def list_records_ids_with_tag(self, tag):
        """List id of all records tagged with the given tag."""
        for record in self.list_records_with_tag(tag):
            yield record['id']

    def search(self, term):
        """Search for a term in records and return the corresponding ids."""
        for record in self.list_records():
            if term in dumps(record):
                yield record['id']

    def search_id(self, partial_id):
        """Search for an id given the first part of an id."""
        for record_id in self.list_record_ids():
            if record_id.startswith(partial_id):
                yield record_id

    def id_from_filename(self, filename):
        """Return the id of the first record matching filename."""
        for record in self.list_records():
            if filename == record['info']['filename']:
                return record['id']

    def __repr__(self):
        """Get a printable description for this inventory."""
        name = self.__class__.__name__
        return "{}".format(name)


class FolderInventory(Inventory):

    """Inventory in a folder accessible via the local filesystem."""

    def __init__(self, path):
        """Initialize a FolderInventory on the given path."""
        self.path = path

    def _record_path(self, id_):
        """Return the path on the filesystem where a record is stored."""
        return os.path.join(self.path, id_ + '.json')

    def list_record_ids(self):
        """List all record ids present in the inventory."""
        for filename in os.listdir(self.path):
            id_ = filename[:-len('.json')]
            yield id_

    def delete(self, id_):
        """Delete a record from the inventory."""
        os.remove(self._record_path(id_))

    def get_record(self, id_):
        """Load metadata for the given id."""
        filepath = self._record_path(id_)
        return loads(open(filepath, 'r').read())

    def save_record(self, record):
        """Save a new record on disk."""
        destination = self._record_path(record['id'])
        open(destination, 'w').write(dumps(record))

    def __repr__(self):
        """Get a printable description for this inventory."""
        name = self.__class__.__name__.replace('Inventory', '')
        return "{}: {}".format(name, self.path)


def load_inventory(settings):
    """Initialize an inventory instance from settings."""
    type_ = settings['type']
    args = settings.get('args', {})

    if type_ == 'FolderInventory':
        return FolderInventory(**args)
