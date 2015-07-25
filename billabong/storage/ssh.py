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

"""Storage implementation based on the SSH protocol."""

import os.path
import paramiko
from .abstract import Storage

from billabong.utils import read_in_chunks


class SSHStorage(Storage):

    """Blob storage on a remote read-write SSH host."""

    def __init__(self, path, host, port=22):
        """Initialize an SSH storage based on the given credentials."""
        self.path = path
        self.host = host
        self.port = port

    def _blob_path(self, id_):
        """Get the path on the filesystem where a blob is stored."""
        return os.path.join(self.path, id_)

    def _ssh_connection(self):
        """Establish an SSH connection using the storage host settings."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=self.port)
        return ssh

    def list_blob_ids(self, *, read_aheads=50):
        """List all ids present in the blobs storage."""
        try:
            ssh = self._ssh_connection()
            sftp = ssh.open_sftp()
            for i in sftp.listdir_iter(self.path, read_aheads=read_aheads):
                yield i.filename
            sftp.close()
        finally:
            ssh.close()

    def import_blob(self, id_, blobfile, callback=None):
        """Add an encrypted blob file to the storage by copying the file."""
        path = self._blob_path(id_)

        try:
            ssh = self._ssh_connection()
            sftp = ssh.open_sftp()
            sftp.putfo(blobfile, path, callback=callback, confirm=True)
            sftp.close()
        finally:
            ssh.close()

    def read_in_chunks(self, id_, offset=0, chunk_size=1024):
        """Read a blob file chunk by chunk."""
        path = self._blob_path(id_)

        try:
            ssh = self._ssh_connection()
            sftp = ssh.open_sftp()

            fdesc = sftp.file(path, mode='r')
            fdesc.seek(offset)

            i = 0
            for chunk in read_in_chunks(fdesc, chunk_size):
                yield (i, chunk)

            sftp.close()
        finally:
            ssh.close()
