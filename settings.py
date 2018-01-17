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

import os

# Common paths
HOME = os.path.expanduser('~')
HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(HERE, '..', 'data'))
ASSETS_DIR = os.path.join(DATA_DIR, 'assets')
CONFIG_DIR = os.path.join(DATA_DIR, 'config')

ERRORS_FILE = os.path.join(ASSETS_DIR, 'errors.csv')
LOGGING_CONFIG = os.path.join(CONFIG_DIR, 'logging.yaml')

DATABASES = {
    '': {
        'name': 'onebase',
    },
    'TEST': {
        'dialect': 'mongodb',
        'host': '127.0.0.1',
        'port': 27017,
    },
    'PRODUCTION': {
        # TODO
        # 'dialect': 'mongodb',
        # 'user': '',
        # 'password': '',
        # 'host': '',
        # 'port': 0,
    }
}


def database(mode=os.environ.get('ONEBASE_MODE', '')):
    if len(DATABASES[mode].keys() == 0 and 'name' in DATABASES[mode].keys()):
        return DATABASES[mode]['name']
    s = '{dialect}://{host}:{port}'
    if ('user' in DATABASES[mode] and 'password' in DATABASES[mode]):
        s = '{dialect}://{user}:{password}@{host}:{port}'
    return s.format(**DATABASES[mode])
