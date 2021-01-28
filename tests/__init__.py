# Copyright 2021 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest


class TestBase(unittest.TestCase):

    _ZERO_ADDRESS = 'hx0000000000000000000000000000000000000000'

    def assertSuccess(self, status: str):
        self.assertEqual(1, int(status, 16))

    def assertFailure(self, status: str):
        self.assertEqual(0, int(status, 16))

    def assertEvents(self, expected: dict, events: list):
        self.assertEqual(len(expected.keys()), len(events))
        for e in events:
            name = e['indexed'][0]
            if name in expected.keys():
                self.assertEqual(e['indexed'][1:] + e['data'], expected[name])
            else:
                self.fail(f'Unexpected event: {e}')

    @staticmethod
    def getLocalEnvs():
        return 'local', 'res/keystore_test1', 'test1_Account'

    @staticmethod
    def getTokenId():
        return int(os.urandom(4).hex(), 16)
