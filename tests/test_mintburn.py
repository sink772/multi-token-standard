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

from random import randint

from iconsdk.exception import JSONRPCException

from scripts.config import Config
from scripts.deploy_contract import deploy
from scripts.score import Score
from tests import TestBase


class TestIRC31MintBurn(TestBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.config = Config(*cls.getLocalEnvs())
        cls.owner = cls.config.owner
        cls.tx_handler = cls.config.tx_handler
        cls.score = Score(cls.tx_handler, deploy(cls.config, 'multi_token'))

    def mint_token(self, wallet, supply: int) -> int:
        _id = self.getTokenId()
        params = {
            '_id': _id,
            '_supply': supply,
            '_uri': f'http://nft.info/{_id}'
        }
        tx_hash = self.score.invoke(wallet, 'mint', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])
        return _id

    def ensure_balance(self, address, _id: int, amount: int):
        balance_params = {
            '_owner': address,
            '_id': _id
        }
        balance = self.score.call('balanceOf', balance_params)
        self.assertEqual(amount, int(balance, 16))

    def test_mint(self):
        _supply = randint(1, 100)
        _id = self.mint_token(self.owner, _supply)
        self.ensure_balance(self.owner.get_address(), _id, _supply)

        # mint with the existing id
        mint_params = {
            '_id': _id,
            '_supply': _supply,
            '_uri': f'http://nft.info/{_id}'
        }
        with self.assertRaises(JSONRPCException):
            self.score.invoke(self.owner, 'mint', mint_params)

    def test_burn(self):
        # burn with invalid token id
        burn_params = {
            '_id': self.getTokenId(),
            '_amount': 1
        }
        with self.assertRaises(JSONRPCException):
            self.score.invoke(self.owner, 'burn', burn_params)

        # mint token
        _supply = randint(2, 100)
        _id = self.mint_token(self.owner, _supply)

        # burn with creator
        burn_params['_id'] = _id
        tx_hash = self.score.invoke(self.owner, 'burn', burn_params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # burn with invalid owner
        alice = self.config.accounts[0]
        with self.assertRaises(JSONRPCException):
            self.score.invoke(alice, 'burn', burn_params)

        # transfer ownership and burn with new owner
        transfer_params = {
            '_from': self.owner.get_address(),
            '_to': alice.get_address(),
            '_id': _id,
            '_value': _supply - 1
        }
        tx_hash = self.score.invoke(self.owner, 'transferFrom', transfer_params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])
        self.ensure_balance(self.owner.get_address(), _id, 0)
        self.ensure_balance(alice.get_address(), _id, _supply - 1)

        tx_hash = self.score.invoke(alice, 'burn', burn_params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])
        self.ensure_balance(alice.get_address(), _id, _supply - 2)
