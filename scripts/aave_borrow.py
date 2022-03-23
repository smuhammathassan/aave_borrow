from brownie import network, config, accounts, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3
from decimal import Decimal


ammount_input = float(input("Enter ammount to deposit: "))
ammount_in_wei = Web3.toWei(ammount_input, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth(ammount_in_wei)
    lending_pool = get_landing_pool()
    approve_tx = approve_erc20(
        ammount_in_wei, lending_pool.address, erc20_address, account
    )
    approve_tx.wait(1)
    print("Depositing ...")
    depositing_tx = lending_pool.deposit(
        erc20_address, ammount_in_wei, account.address, 0, {"from": account}
    )
    depositing_tx.wait(1)
    print("Deposited ...!")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("Lets Borrow ...")
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    amount_dai_to_borrow = (1 / dai_eth_price) * Decimal(borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI ...!")
    get_borrowable_data(lending_pool, account)


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_price = Web3.fromWei(latest_price, "ether")
    print(f"latest price of DAI/ETH is {converted_price}")
    return converted_price


def get_borrowable_data(landing_pool, account):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = landing_pool.getUserAccountData(account.address)
    converted_totalCollateralETH = Web3.fromWei(totalCollateralETH, "ether")
    converted_totalDebtETH = Web3.fromWei(totalDebtETH, "ether")
    converted_availableBorrowsETH = Web3.fromWei(availableBorrowsETH, "ether")
    print(f"You have {converted_totalCollateralETH} eth as a collateral")
    print(f"You are {converted_totalDebtETH} eth in debt.")
    print(f"You can still borrow {converted_availableBorrowsETH} worth of eth")
    return (float(converted_availableBorrowsETH), float(converted_totalDebtETH))


def get_landing_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx
