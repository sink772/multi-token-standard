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

from iconsdk.libs.in_memory_zip import gen_deploy_data_content

from scripts.config import Config

USE_JAVA_IMPL = False


def print_empty(*args):
    pass


def get_score_content(target: str):
    score_path = f"./contracts/{target}"
    return gen_deploy_data_content(score_path)


def deploy(config: Config, target: str, verbose=print_empty):
    owner = config.owner
    tx_handler = config.tx_handler
    verbose(">>> owner address:", owner.get_address())

    if USE_JAVA_IMPL and target == 'multi_token':
        jar_path = './irc31-token-0.1.0-optimized.jar'
        content = gen_deploy_data_content(jar_path)
        content_type = 'application/java'
    else:
        content = get_score_content(target)
        content_type = 'application/zip'
    verbose(">>> content size =", len(content))
    tx_hash = tx_handler.install(owner, content, content_type)
    verbose(">>> deploy txHash:", tx_hash)

    tx_result = tx_handler.ensure_tx_result(tx_hash, verbose != print_empty)
    score_address = tx_result["scoreAddress"]
    verbose(">>> scoreAddress:", score_address)
    # print(">>> api =", tx_handler.get_score_api(score_address))
    return score_address
