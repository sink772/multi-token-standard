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

from time import sleep

from iconsdk.builder.transaction_builder import (
    CallTransactionBuilder, DeployTransactionBuilder, TransactionBuilder
)
from iconsdk.signed_transaction import SignedTransaction

from . import die, print_response


class TxHandler:
    ZERO_ADDRESS = "cx0000000000000000000000000000000000000000"

    def __init__(self, service, nid):
        self._icon_service = service
        self._nid = nid

    def _deploy(self, wallet, to, content, params, limit):
        transaction = DeployTransactionBuilder() \
            .from_(wallet.get_address()) \
            .to(to) \
            .nid(self._nid) \
            .step_limit(limit) \
            .content_type("application/zip") \
            .content(content) \
            .params(params) \
            .build()
        return self._icon_service.send_transaction(SignedTransaction(transaction, wallet))

    def install(self, wallet, content, params=None, limit=0x50000000):
        return self._deploy(wallet, self.ZERO_ADDRESS, content, params, limit)

    def update(self, wallet, to, content, params=None, limit=0x70000000):
        return self._deploy(wallet, to, content, params, limit)

    def _send_transaction(self, transaction, wallet, limit):
        if limit is not None:
            signed_tx = SignedTransaction(transaction, wallet, limit)
        else:
            estimated_step = self._icon_service.estimate_step(transaction)
            signed_tx = SignedTransaction(transaction, wallet, estimated_step)
        return self._icon_service.send_transaction(signed_tx)

    def invoke(self, wallet, to, method, params, limit=None):
        transaction = CallTransactionBuilder() \
            .from_(wallet.get_address()) \
            .to(to) \
            .nid(self._nid) \
            .method(method) \
            .params(params) \
            .build()
        return self._send_transaction(transaction, wallet, limit)

    def transfer(self, wallet, to, amount, limit=100000):
        transaction = TransactionBuilder() \
            .from_(wallet.get_address()) \
            .to(to) \
            .nid(self._nid) \
            .value(amount) \
            .build()
        return self._send_transaction(transaction, wallet, limit)

    def ensure_tx_result(self, tx_hash):
        count = 5
        while True:
            result = self._icon_service.get_transaction_result(tx_hash, True)
            if 'error' in result:
                count -= 1
                if count <= 0:
                    print_response("Response", result['error'])
                    die('Error: failed to get transaction result')
                sleep(2)
            elif 'result' in result:
                result = result['result']
                print_response("Result", result)
                if result['status'] != '0x1':
                    die('Error: transaction failed')
                return result
            else:
                print_response("Response", result)
                die(f'Error: unknown response')