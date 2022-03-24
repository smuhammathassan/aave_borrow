from scripts.helpful_scripts import get_account
from brownie import interface, network, config
from web3 import Web3


def get_weth(amount):

    """
    Deposit eth and get weth

    For that we will be needing address and abi

    """

    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": amount})
    tx.wait(1)
    print(f"Recived {Web3.fromWei(amount, 'ether')} Weth")
    return tx


def main():
    get_weth()
