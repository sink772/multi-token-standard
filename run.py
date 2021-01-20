#!/usr/bin/env python

import argparse

from scripts.deploy_contract import deploy


class Command:

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(title='Available commands', dest='command')
        subparsers.required = True
        subparsers.add_parser('deploy')

        args = parser.parse_args()
        getattr(self, args.command)(args)

    @staticmethod
    def deploy(args):
        deploy()


if __name__ == "__main__":
    Command()
