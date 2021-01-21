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

from scripts.config import Config
from scripts.deploy_contract import deploy
from scripts.score import Score
from tests import TestBase


class TestIRC31Mintable(TestBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.owner = Config().owner
        cls.tx_handler = Config().tx_handler
        cls.score = Score(cls.tx_handler, deploy('multi_token'))

    def test_mint(self):
        _id = self._getTokenId()
        _supply = randint(1, 100)
        params = {
            '_id': _id,
            '_supply': _supply,
            '_uri': f'http://nft.info/{_id}'
        }
        tx_hash = self.score.invoke(self.owner, 'mint', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        params2 = {
            '_owner': self.owner.get_address(),
            '_id': _id
        }
        balance = self.score.call('balanceOf', params2)
        self.assertEqual(_supply, int(balance, 16))

        # mint with the existing id
        step_used = int(tx_result['stepUsed'], 16)
        tx_hash = self.score.invoke(self.owner, 'mint', params, step_used)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertFailure(tx_result['status'])
