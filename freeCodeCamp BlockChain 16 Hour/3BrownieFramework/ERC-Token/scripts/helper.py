from brownie import network, accounts, config

FORKED_LOCAL_ENVS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local"]

DECIMALS = 8  # So sending decimal will be 8
STARTING_PRICE = 200000000000  # Decimal is 8 so that's why adding extra 8 zeros


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(
            id
        )  # Loading account which we added in env account by account create command

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVS
        or network.show_active() in FORKED_LOCAL_ENVS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])
