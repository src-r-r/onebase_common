#!/usr/bin/env python3
"""
This file is part of nose-json-formatter.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with nose-json-formatter.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging

from unittest import (
    TestResult,
    TextTestRunner,
)

logger = logging.getLogger('')


def JsonTestResult(TestResult):

    def __init__(self, *args, **kwargs):
        super(JsonTestResult, self).__init__(*args, **kwargs)
        self.json_data = {
            'errors': [],
            'fail': [],
            'pass': [],
            'skip': [],
            'expected_fail': [],
            'unexpected_pass': [],
        }

    def _add_to(self, key, item):
        self.json_data[key].append(item)

    def _jsonify_test(self, test):
        return {
            'address': test.address(),
            'context': test.context,
            'id': test.id(),
        },

    def _add_bad_thing(self, key, test, error):
        (t, v, tb) = error
        self._add_to(key, {
            'test': self._jsonify_test(test),
            'error': {'type': t, 'value': v, 'traceback': tb, },
        })

    def addError(self, test, error):
        """ Add an error to the final output. """
        self._add_bad_thing('errors', test, error)

    def addFailure(self, test, error):
        """ Add a failure to the final output. """
        self._add_bad_thing('fail', test, error)

    def addSuccess(self, test):
        """ Add a success to the final output. """
        self._add_to('pass', self._jsonify_test(test))

    def addSkip(self, test, reason):
        self._add_to('skip', {
            'test': self._jsonify_test(test),
            'reason': reason,
        })

    def addExpectedFailure(self, test, err):
        self._add_bad_thing('expeceted_fail', test, err)

    def addUnexpectedSuccess(self, test):
        self._add_to('unexpected_pass', self._jsonify_test(test))

    def printErrors(self):
        logger.error('errors: {}'.format(self.json_data['errors']))


class JsonTestRunner(TextTestRunner):

    def __init__(self, **kwargs):
        kwargs['resultclass'] = JsonTestResult
        super(JsonTestRunner, self).__init__(**kwargs)
