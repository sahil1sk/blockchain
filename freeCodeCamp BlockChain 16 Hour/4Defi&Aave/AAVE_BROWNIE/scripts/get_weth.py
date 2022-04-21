from scripts.helper import get_account
from brownie import interface, config, network


def main():
    get_weth()


# WETH of Aave (In which address we deposit money)
def get_weth():
    # ABI, Adress
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit(
        {
            "from": account,
            "value": 0.1 * 10**18,
            "gas_limit": 1000000,
            "allow_revert": True,
        }
    )
    tx.wait(1)
    print(f"Received 0.1 WETH")
    return tx
