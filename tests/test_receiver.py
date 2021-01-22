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

from iconsdk.exception import JSONRPCException

from scripts.config import Config
from scripts.deploy_contract import deploy
from scripts.score import Score
from tests import TestBase


class TestIRC31Receiver(TestBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.owner = Config().owner
        cls.tx_handler = Config().tx_handler
        cls.multi_token = Score(cls.tx_handler, deploy('multi_token'))
        cls.receiver = Score(cls.tx_handler, deploy('token_receiver'))

    def mint_token(self, token: Score, supply: int):
        _id = self._getTokenId()
        params = {
            '_id': _id,
            '_supply': supply,
            '_uri': f'http://nft.info/{_id}'
        }
        tx_hash = token.invoke(self.owner, 'mint', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])
        return _id

    def test_01_setOriginator(self):
        params = {
            '_origin': self.multi_token.address,
            '_approved': True
        }
        tx_hash = self.receiver.invoke(self.owner, 'setOriginator', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # Not an owner
        alice = Config().accounts[0]
        with self.assertRaises(JSONRPCException):
            self.receiver.invoke(alice, 'setOriginator', params)

        # Invalid contract address
        params['_origin'] = alice.get_address()
        with self.assertRaises(JSONRPCException):
            self.receiver.invoke(self.owner, 'setOriginator', params)

    def test_02_onReceived(self):
        supply = 100
        _id = self.mint_token(self.multi_token, supply)
        params = {
            '_from': self.owner.get_address(),
            '_to': self.receiver.address,
            '_id': _id,
            '_value': int(supply / 2)
        }
        tx_hash = self.multi_token.invoke(self.owner, 'transferFrom', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # invoked from an unregistered contract
        unknown_token = Score(self.tx_handler, deploy('multi_token'))
        _id = self.mint_token(unknown_token, supply)
        params['_id'] = _id
        with self.assertRaises(JSONRPCException):
            unknown_token.invoke(self.owner, 'transferFrom', params)

    def test_03_onBatchReceived(self):
        supply = 100
        ids = []
        for i in range(3):
            _id = self.mint_token(self.multi_token, supply)
            ids.append(_id)
        values = [50, 60, 70]
        params = {
            '_from': self.owner.get_address(),
            '_to': self.receiver.address,
            '_ids': ids,
            '_values': values
        }
        tx_hash = self.multi_token.invoke(self.owner, 'transferFromBatch', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])
