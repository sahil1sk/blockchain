from brownie import network, accounts, config

FORKED_LOCAL_ENVS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local"]


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
