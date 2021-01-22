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

from iconservice import *


def require(condition: bool, message: str):
    if not condition:
        revert(message)


class SampleTokenReceiver(IconScoreBase):

    def __init__(self, db: 'IconScoreDatabase') -> None:
        super().__init__(db)
        # allowlist of token contracts
        self._originators = DictDB('originators', db, value_type=bool)

    def on_install(self) -> None:
        pass

    def on_update(self) -> None:
        pass

    @external
    def setOriginator(self, _origin: Address, _approved: bool):
        require(self.owner == self.msg.sender, "Not contract owner")
        require(_origin.is_contract, "Not contract address")
        self._originators[_origin] = _approved

    @external
    def onIRC31Received(self, _operator: Address, _from: Address, _id: int, _value: int, _data: bytes):
        """
        A method for handling a single token type transfer, which is called from the multi token contract.
        It works by analogy with the fallback method of the normal transactions and returns nothing.
        Throws if it rejects the transfer.

        :param _operator: The address which initiated the transfer
        :param _from: the address which previously owned the token
        :param _id: the ID of the token being transferred
        :param _value: the amount of tokens being transferred
        :param _data: additional data with no specified format
        """
        require(self._originators[self.msg.sender], "Unrecognized token contract")
        self.IRC31Received(self.msg.sender, _operator, _from, _id, _value, _data)

    @external
    def onIRC31BatchReceived(self, _operator: Address, _from: Address, _ids: List[int], _values: List[int], _data: bytes):
        """
        A method for handling multiple token type transfers, which is called from the multi token contract.
        It works by analogy with the fallback method of the normal transactions and returns nothing.
        Throws if it rejects the transfer.

        :param _operator: The address which initiated the transfer
        :param _from: the address which previously owned the token
        :param _ids: the list of IDs of each token being transferred (order and length must match `_values` list)
        :param _values: the list of amounts of each token being transferred (order and length must match `_ids` list)
        :param _data: additional data with no specified format
        """
        require(self._originators[self.msg.sender], "Unrecognized token contract")
        for i in range(len(_ids)):
            _id = _ids[i]
            _value = _values[i]
            self.IRC31Received(self.msg.sender, _operator, _from, _id, _value, _data)

    @eventlog(indexed=3)
    def IRC31Received(self, _origin: Address, _operator: Address, _from: Address, _id: int, _value: int, _data: bytes):
        pass
