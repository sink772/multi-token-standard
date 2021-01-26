#!/usr/bin/env python

import argparse

from scripts.config import Config
from scripts.deploy_contract import deploy


class Command:

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--endpoint', type=str, default='local', help='target endpoint for connection')
        parser.add_argument('-k', '--keystore', type=argparse.FileType('r'), default='res/keystore_test1',
                            help='keystore file for creating transactions')
        subparsers = parser.add_subparsers(title='Available commands', dest='command')
        subparsers.required = True

        deploy_parser = subparsers.add_parser('deploy')
        deploy_parser.add_argument('contract', type=str, help='target contract to deploy')

        args = parser.parse_args()
        getattr(self, args.command)(args)

    @staticmethod
    def deploy(args):
        config = Config(args.endpoint, args.keystore.name)
        deploy(config, args.contract, print)


if __name__ == "__main__":
    Command()
