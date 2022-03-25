from brownie import network, config, accounts, interface
from scripts.helpful_scripts import get_account
from scripts.aave_borrow import get_landing_pool, get_borrowable_data
from scripts.get_weth import get_weth
from web3 import Web3
from decimal import Decimal


def main():
    account = get_account()
    lending_pool = get_landing_pool()
    get_borrowable_data(lending_pool, account)
