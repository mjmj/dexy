#!/usr/bin/env python3

import argparse
import json
import os
import logging
import time

from config import development
from config import production
from web3 import Web3, WebsocketProvider

# arguments
parser = argparse.ArgumentParser(description="RDS Global DB failover")
parser.add_argument("host", metavar="HOST",
                    help="Hosted node to connect to")
parser.add_argument("-v", help="Specify log level verbosity defaults to INFO",
                    dest="verbosity", default="INFO")
parser.add_argument("-e", "--environment", help="Test environment")
args = parser.parse_args()

# logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/dexy.log', encoding='utf-8',
                    level=args.verbosity)

class NotConnectedException(Exception):
    pass

class EnvironmentNotSetException(Exception):
    pass


def get_accounts():
    return w3.eth.accounts

def get_config(env):
    if not env:
        raise EnvironmentNotSetException()

    if env == 'prod' or 'production':
        return production
    else:
        return development

def get_env(env, default=None):
    logger.info(f"Environment is {env}")
    return env or default

def check_connection(node):
    if not w3.isConnected():
        raise NotConnectedException(
            f"Unable to connect to node {node}")
    else:
        logger.info(f"Connected to {node}")



if __name__ == '__main__':
    env = get_env(args.environment)
    config = get_config(env)
    host_url = config.config['url']
    w3 = Web3(Web3.WebsocketProvider(host_url))

    check_connection(w3)
    if not get_accounts():
        logger.info(f"Creating an erc-20 address")

