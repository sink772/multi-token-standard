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

from iconsdk.libs.in_memory_zip import gen_deploy_data_content

from util import get_icon_service, load_keystore
from util.txhandler import TxHandler


def get_score_content():
    score_path = "./contracts"
    return gen_deploy_data_content(score_path)


def main():
    icon_service, nid = get_icon_service('local')
    owner_wallet = load_keystore("res/keystore_test1", "test1_Account")
    print(">>> owner address: ", owner_wallet.get_address())

    tx_handler = TxHandler(icon_service, nid)
    content = get_score_content()
    tx_hash = tx_handler.install(owner_wallet,
                                 content)
    print(">>> deploy txHash:", tx_hash)

    tx_result = tx_handler.ensure_tx_result(tx_hash)
    score_address = tx_result["scoreAddress"]
    print(">>> scoreAddress:", score_address)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('exit')
