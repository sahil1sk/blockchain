import os
from brownie import accounts, config, network, SimpleStorage


def deploy_simple_storage():
    # Load account from prebuilt brownie accounts
    # account = accounts[0]  # Using account 0

    # If you want to use your created account like Meta Mask account
    # Add it into the brownie account by => brownie accounts new account_name
    # account = accounts.load("account-name")

    # Use account from env
    # account = accounts.add(os.getenv("PRIVATE_KEY"))

    # To get account from config
    # account = accounts.add(config["wallets"]["from_key"])

    account = get_account()

    # Deploy SimpleStorage contract (Brownie now wheather it is transaction or Simple Call)
    ss = SimpleStorage.deploy({"from": account})
    print(ss.retrieve())  # Simple Call (Initial value is 0)

    # Storing data and waiting for one block
    transaction = ss.store(10, {"from": account})
    transaction.wait(1)

    print(ss.retrieve())  # Simple Call for getting changed value


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    print("Main function started....")
    deploy_simple_storage()
