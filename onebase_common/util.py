#!/usr/bin/env python3
"""
This file is part of 1Base.

1Base is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

1Base is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with 1Base.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging

from urllib.parse import urlparse, urljoin
from urllib import parse
from flask import request, url_for
import hashlib

logger = logging.getLogger(__name__)

class idict(dict):
    """ Dict with (ordered) automatic iteration. """
    def __iter__(self):
        return ((i, self.get(i)) for i in sorted(self.keys()))

    def append(self, item):
        try:
            i = max(sorted(self.keys()))
        except Exception as e:
            logger.error(e)
            i = 0
        self[i] = item

def is_safe_url(target):
    """ Checks if `target` is a safe URL.

    Snippet from http://flask.pocoo.org/snippets/62/

    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def hashpass(s, method='sha256'):
    """ For those who don't like to handle crypto. """
    return getattr(hashlib, method)(s.encode('ascii')).hexdigest()


def path_split(path, sep='/', max=0):
    """ Split a path, ignoring empty path parts (e.g. '').

    :param path: Full path to split (e.g. /path/to/node)

    :param sep: Seperator character (e.g. '/')

    :param max: Maximum splits to perform. (0=infinite)

    :return: list representing path parts, negating nullish items.
    """
    if max == 0:
        return [p for p in path.split(sep) if len(p.strip()) > 0]
    else:
        return [p for p in path.split(sep, max) if len(p.strip()) > 0]


def path_head_tail(path, sep='/'):
    """ Convenience method to split a path once, leaving a head and a tail.

    For example `path_head_tail('/path/to/node')` -> ('path', 'to/node')
    """
    if path.startswith(sep):
        path = path[1:]
    if sep not in path:
        return (path, None)
    return path_split(path, sep, 1)


def path_is_parent(path, other, sep='/'):
    """ True if path is a parent path of other. """
    parts = path_split(path, sep=sep)
    other_parts = path_split(path, sep=sep)
    if len(parts) > len(other_parts):
        return False
    for (i, p) in enumerate(parts):
        if p != other_parts[i]:
            return False
    return True


def unparse_qs(q):
    """ Revert query dict back to query string. """
    return '&'.join(['{}={}'.format(k, ','.join(v)) for (k, v) in q.items()])


def reconstruct_url(request, updated_args):
    """ Extract the request, update the args, then repack the URL.

    :param request: Flask request object.

    :param updated args: Keys to update final URL

    :return: Full URL modified with updated_args
    """
    parts = parse.urlsplit(request.url)
    query = parse.parse_qs(parts.query)
    query.update(updated_args)
    parts_out = (parts.scheme, parts.netloc, parts.path,
                 unparse_qs(query), parts.fragment)
    return parse.urlunsplit(parts_out)
