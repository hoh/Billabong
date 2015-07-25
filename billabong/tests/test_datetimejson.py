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

"""Tests JSON handling of datetime objects."""

import json
from datetime import datetime
from billabong.utils import json_handler


def test_encode_datetime():
    """Test dumping of datetime object in JSON."""
    dico = {'date': datetime(2015, 4, 8)}
    assert json.dumps(dico, default=json_handler) \
        == '{"date": "2015-04-08T00:00:00"}'


def test_encode_datetime_subdico():
    """Test dumping of datetime object in a sub-dictionnary in JSON."""
    dico = {'date': {'good': True, 'time': datetime(2015, 4, 8)}}
    encoded = json.dumps(dico, default=json_handler)
    assert '"time": "2015-04-08T00:00:00"' in encoded
