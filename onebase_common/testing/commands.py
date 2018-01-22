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

from setuptools.command.test import test as st_test
from onebase_common.testing.format import JsonTestResult, JsonTestRunner

class test(st_test):

    def run_test(self):
        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if six.PY3 and getattr(self.distribution, 'use_2to3', False):
            module = self.test_suite.split('.')[0]
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                list(map(sys.modules.__delitem__, del_modules))

        test = unittest.main(
            None, None, self._argv,
            testLoader=self._resolve_as_ep(self.test_loader),
            testRunner=JsonTestRunner,
            exit=False,
        )
        if not test.result.wasSuccessful():
            msg = 'Test failed: %s' % test.result
            self.announce(msg, log.ERROR)
            raise DistutilsError(msg)
