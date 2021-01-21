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

from unittest import TestCase

from contracts.util.rlp import rlp_encode_bytes, rlp_encode_list, int_to_bytes
from scripts.util.rlp import rlp_decode


class TestRLP(TestCase):

    def test_encode_to_decode(self):
        data = [0, 1, 64, 100, 1000]
        bs = rlp_encode_list(data)
        items = rlp_decode(bs)
        for i in range(len(items)):
            self.assertEqual(int_to_bytes(data[i]), rlp_decode(items[i]))

    def test_encode_bytes(self):
        tests = [
            [b'', bytes([0x80])],
            [b'cat', bytes([0x83, 0x63, 0x61, 0x74])],
            [bytes([0x7f]), bytes([0x7f])],
            [bytes([0x80, 0xff]), bytes([0x82, 0x80, 0xff])],
            [bytes([0x11]*55), bytes([0x80+55]+[0x11]*55)],
            [bytes([0x11]*56), bytes([0xB7+1, 56]+[0x11]*56)],
            [bytes([0x11]*256), bytes([0xB7+2, 0x01, 0x00]+[0x11]*256)]
        ]
        for t in tests:
            try:
                self.assertEqual(t[1], rlp_encode_bytes(t[0]))
            except:
                print(f"FAIL on encoding(src={t[0]},exp={t[1]})")
                raise

    def test_encode_list(self):
        tests = [
            [[], bytes([0xc0])],
            [[1, 2, 3], bytes([0xc3, 0x01, 0x02, 0x03])],
            [[0x636174, 0x646f67], bytes([0xc8, 0x83, 0x63, 0x61, 0x74, 0x83, 0x64, 0x6f, 0x67])],
        ]
        for t in tests:
            try:
                self.assertEqual(t[1], rlp_encode_list(t[0]))
            except:
                print(f"FAIL on encoding(src={t[0]},exp={t[1]})")
                raise
