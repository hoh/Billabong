# Copyright (c) 2016 "Hugo Herter http://hugoherter.com"
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


"""Archive of inventory data."""

from zipfile import ZipFile
from billabong.utils import dumps


class Archive:

    """Archive an inventory - abstract class."""

    def __init__(self, path):
        self.path = path

    def update(self, inventory):
        """Save all records from the inventory in an archive."""
        raise NotImplementedError

    def restore(self, inventory):
        """Restore all records from an archive into the inventory."""
        raise NotImplementedError


class NotEncryptedZipArchive(Archive):

    """Archive in an unencrypted zip file."""

    def update(self, inventory):
        """Save all records from the inventory in a zipfile on self.path."""
        with ZipFile(self.path, mode='w') as zipfile:
            for record_id in inventory.list_record_ids():
                zipfile.writestr(
                    "{}.json".format(record_id),
                    dumps(inventory.get_record(record_id), indent=4),
                )
