#!/usr/bin/env python3

"""
This file is part of 1Base.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with 1Base.  If not, see <http://www.gnu.org/licenses/>.
"""

from logging import Formatter
from json import dumps

class JsonFormatter(Formatter):

    def __init__(self, attributes=None, datefmt=None, style='%'):
        self.attributes = attributes
        super(JsonFormatter, self).__init__(datefmt=datefmt, style=style)

    def format(self, record):
        data = {}
        if self.attributes is not None:
            for a in self.attributes:
                data[a] = getattr(record, a)
        for a in record.vars().items():
            if any((a.startswith('_'), )):
                continue
            data[a] = getattr(record, a)
        return dumps(record)
