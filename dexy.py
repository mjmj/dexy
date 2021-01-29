#!/usr/bin/env python3

import argparse
import json
import logging
import os
import time

from eth_account import Account
from eth_utils import decode_hex, to_checksum_address
from web3 import Web3, WebsocketProvider

from accounts import infura, rinkeby
from common import *
from config import development, production
from dexs import one_inch

# arguments
parser = argparse.ArgumentParser(description="RDS Global DB failover")
parser.add_argument("-e", "--environment", required=True, help="Test environment")
parser.add_argument("-c", "--connection", required=True, help="Connection type: local, https or wss")
parser.add_argument("-d", "--dex", required=True, help="Dex to trade on")
parser.add_argument("-v", help="Specify log level verbosity defaults to INFO", dest="verbosity", default="INFO")
args = parser.parse_args()

# secret env vars
ACCOUNT_RANDOMNESS = os.getenv('ACCOUNT_RANDOMNESS')
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
INFURA_PROJECT_SECRET = os.getenv('INFURA_PROJECT_SECRET')

# logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/dexy.log', encoding='utf-8',
                    level=args.verbosity)

class NotConnectedException(Exception):
    pass

class EnvironmentNotSetException(Exception):
    pass


def check_connection(node):
    if w3.isConnected():
        logger.info(f"We are connected to {url}")
    if not w3.isConnected():
        raise NotConnectedException(f"Unable to connect to node {node}")

def create_account():
    acct = Account.create(ACCOUNT_RANDOMNESS)
    return acct

def get_config(env):
    if not env:
        raise EnvironmentNotSetException()

    if env == 'prod' or env == 'production':
        return production
    else:
        return development

def get_env(env):
    logger.info(f"Environment is {env}")
    return env

def get_url(config):
    con = args.connection
    if con == 'wss' or con == 'websocket':
        return config.config['websocket_url'] + INFURA_PROJECT_ID
    elif con == 'local':
        return config.config['local_url'] + INFURA_PROJECT_ID
    else:
        return config.config['https_url']

def get_connection(url):
    # There's better ways to do this
    if 'http' in url or 'local' in url:
        con = Web3(Web3.HTTPProvider(url))
    elif 'wss' in url:
        con = Web3(Web3.WebsocketProvider(url))
    return con

def get_account_balance(account):
    b = w3.eth.getBalance(account)
    return Web3.fromWei(b, 'ether')

def get_expected_return(from_token, to_token, amount, parts, disable_flags):
    contract_response = dex.functions.getExpectedReturn(
        from_token,
        to_token,
        amount,
        parts,
        disable_flags).call({'from': account_address})
    return contract_response

if __name__ == '__main__':
    env = get_env(args.environment)
    config = get_config(env)
    url = get_url(config)
    w3 = get_connection(url)

    check_connection(w3)

    if not w3.eth.accounts:
        logger.info(f"Creating an erc-20 address")
    account = create_account()
    account_address = account._address
    account_pk = account._private_key
    logger.info(account_address)
    logger.info(account_pk)

    # config lookups
    # dex_config = getattr(dexs, args.dex)

    abi = one_inch.one_inch_abi
    exchange_addr = one_inch.one_inch['exchange_addr']

    dex = w3.eth.contract(
        address=exchange_addr,
        abi=abi
    )

    account_address = Web3.toChecksumAddress('YOUR_ADDRESS')
    print(account_address)
    print(get_account_balance(account_address))
    print(get_expected_return(zrx_token, eth_token, 100, 100, 0))
