from brownie import network, config, accounts, interface
from scripts.helpful_scripts import get_account
from web3 import Web3
from scripts.aave_borrow import get_landing_pool

ammount_input = float(input("Enter ammount to deposit: "))
ammount_in_wei = Web3.toWei(ammount_input, "ether")

def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    lending_pool = get_landing_pool()


function flashLoan(address receiverAddress, address[] calldata assets, uint256[] calldata amounts, uint256[] modes, address onBehalfOf, bytes calldata params, uint16 referralCode)


