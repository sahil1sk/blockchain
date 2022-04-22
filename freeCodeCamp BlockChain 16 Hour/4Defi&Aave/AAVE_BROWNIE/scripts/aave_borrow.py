from brownie import config, network, interface
from scripts.get_weth import get_weth
from scripts.helper import FORKED_LOCAL_ENVS, get_account
from web3 import Web3

# 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in FORKED_LOCAL_ENVS:
        get_weth()
    lending_pool = get_lending_pool()
    print(f"Lending pool address: {lending_pool.address}")
    # Approve sending out ERC-TOKEN FIRST
    print("Approving")
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing..")
    # 0 refereal code it is depricated in latest version so set it as 0
    tx = lending_pool.deposit(
        erc20_address,
        amount,
        account.address,
        0,
        {
            "from": account,
            "gas_limit": 1000000,
            "allow_revert": True,
        },
    )
    tx.wait(1)
    print(f"Deposited {amount} {erc20_address}")
    # Getting data from collectral pool how much we can borrow
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)


# getting 1 dai of how much eth price from aggregator interface
def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)


# Getting all data from the collectral pool
def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(
        spender,
        amount,
        {
            "from": account,
            "gas_limit": 1000000,
            "allow_revert": True,
        },
    )
    tx.wait(1)
    print(f"Approved {amount} {erc20_address} to {spender}")
    return tx


# ILendingPoolAddressesProvider interface only work with Kovana network and mainnet
# so only test it with mainnet fork and kovana network
def get_lending_pool():
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
