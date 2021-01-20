# Copyright 2020 ICON Foundation
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


class TestIRC31Basic(TestBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.owner = Config().owner
        cls.tx_handler = Config().tx_handler
        cls.score = Score(cls.tx_handler, deploy())

    def mint_token(self, supply):
        _id = self._getTokenId()
        params = {
            '_id': _id,
            '_supply': supply,
            '_uri': f'http://nft.info/{_id}'
        }
        tx_hash = self.score.invoke(self.owner, 'mint', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])
        return _id

    def ignore_test_transferFrom(self):
        supply = 100
        _id = self.mint_token(supply)
        alice = Config().accounts[0]
        params = {
            '_from': self.owner.get_address(),
            '_to': alice.get_address(),
            '_id': _id,
            '_value': supply
        }
        tx_hash = self.score.invoke(self.owner, 'transferFrom', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # balance check
        for owner, exp in [(self.owner.get_address(), 0),
                           (alice.get_address(), supply)]:
            params2 = {
                '_owner': owner,
                '_id': _id
            }
            balance = self.score.call('balanceOf', params2)
            self.assertEqual(exp, int(balance, 16))

        # fail case: alice => bob by owner
        bob = Config().accounts[1]
        params['_from'] = alice.get_address()
        params['_to'] = bob.get_address()
        with self.assertRaises(JSONRPCException):
            self.score.invoke(self.owner, 'transferFrom', params)

        # approve owner to transfer alice's token
        params3 = {
            '_operator': self.owner.get_address(),
            '_approved': True
        }
        tx_hash = self.score.invoke(alice, 'setApprovalForAll', params3)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # success case: retry alice => bob by owner
        tx_hash = self.score.invoke(self.owner, 'transferFrom', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # balance check
        for owner, exp in [(self.owner.get_address(), 0),
                           (alice.get_address(), 0),
                           (bob.get_address(), supply)]:
            params2 = {
                '_owner': owner,
                '_id': _id
            }
            balance = self.score.call('balanceOf', params2)
            print(">> bal=", balance)
            self.assertEqual(exp, int(balance, 16))

    def test_transferFromBatch(self):
        supply = 100
        ids = []
        for i in range(3):
            _id = self.mint_token(supply)
            ids.append(_id)
        alice = Config().accounts[0]
        values = [50, 60, 70]
        params = {
            '_from': self.owner.get_address(),
            '_to': alice.get_address(),
            '_ids': ids,
            '_values': values
        }
        tx_hash = self.score.invoke(self.owner, 'transferFromBatch', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # balance check
        for i in range(3):
            params2 = {
                '_owner': alice.get_address(),
                '_id': ids[i]
            }
            balance = self.score.call('balanceOf', params2)
            self.assertEqual(values[i], int(balance, 16))

        # fail case: alice => bob by owner
        bob = Config().accounts[1]
        values2 = [10, 20, 30]
        params['_from'] = alice.get_address()
        params['_to'] = bob.get_address()
        params['_values'] = values2
        with self.assertRaises(JSONRPCException):
            self.score.invoke(self.owner, 'transferFromBatch', params)

        # approve owner to transfer alice's token
        params3 = {
            '_operator': self.owner.get_address(),
            '_approved': True
        }
        tx_hash = self.score.invoke(alice, 'setApprovalForAll', params3)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # success case: retry alice => bob by owner
        tx_hash = self.score.invoke(self.owner, 'transferFromBatch', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # balanceBatch check
        params2 = {
            '_owners': [self.owner.get_address(),
                        alice.get_address(),
                        bob.get_address()],
            '_ids': ids
        }
        exp = [hex(50), hex(40), hex(30)]
        balances = self.score.call('balanceOfBatch', params2)
        self.assertTrue(exp == balances)
