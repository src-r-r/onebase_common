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
import secrets
import yaml

# Common paths
HOME = os.path.expanduser('~')
HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(HERE, '..', 'data'))
ASSETS_DIR = os.path.join(DATA_DIR, 'assets')
CONFIG_DIR = os.path.join(DATA_DIR, 'config')

ERRORS_FILE = os.path.join(ASSETS_DIR, 'errors.csv')
LOGGING_CONFIG = os.path.join(CONFIG_DIR, 'logging.yaml')

ONEBASE_DEV = 'development'
ONEBASE_TEST = 'test'
ONEBASE_PROD = 'production'
ONEBASE_MODE_CHOICES = (ONEBASE_DEV, ONEBASE_TEST, ONEBASE_PROD)
ONEBASE_MODE = os.environ.get('ONEBASE_MODE', ONEBASE_DEV)


if ONEBASE_MODE == ONEBASE_DEV:
    PUBLIC_DATA_DIR = os.path.join(HOME, '.share', 'onebase')
else:
    PUBLIC_DATA_DIR = os.path.join('/etc', 'onebase')

CONFIG_FILE = os.path.join(PUBLIC_DATA_DIR, 'config.yaml')

REQUIRED_FILES = (CONFIG_FILE, )

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(CONFIG_FILE):
    raise RuntimeError('Could not find file {}'.format(CONFIG_FILE))

# load the configuration from the YAML comfing
CONFIG = {}
with open(CONFIG_FILE, 'r') as config_file:
    CONFIG = yaml.load(config_file.read())

""" API Version
"""
API_VERSION = '0.1'

"""" Keywords that are automatically omitted from JSON output. """
DEFAULT_JSON_OMIT = ['objects', ]

""" List of groups that have all permissions.

A permission check will not occur in this instance; only a group name check.
"""
ADMIN_GROUPS = ['admin', ]


RESPONSE_INFO = {
    'copyright': 'Copyright (c) 2017 by 1Base',
    'url': 'TBD',
    'license': 'GPLv3',
    'version': API_VERSION,
}

###
# Crypto settings
###

""" Secret token used for Flask sessions.
"""
FLASK_SECRET = secrets.token_urlsafe()


def configure_database(db_config):
    """ Configure the mongo database given the configuraton in the YAML
    configuration file.
    """
    if (len(db_config.keys()) == 1) and ('name' in db_config.keys()):
        return db_config['name']
    s = '{dialect}://{host}:{port}'
    if ('user' in db_config and 'password' in db_config):
        s = '{dialect}://{user}:{password}@{host}:{port}'
    return s.format(**db_config)


DATABASE = configure_database(CONFIG['database'][CONFIG['mode']])
