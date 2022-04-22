from brownie import (
    network,
    accounts,
    config,
)
import eth_utils  # pip install eth_utils

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


# initalizer=box.store, 1,2,3, [* args means number of arguments]
def encode_fun_data(initalizer=None, *args):
    """Encodes the function call so we can work with an initializer

    Args:
        initalizer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call, Example: 'box.store',
        Defaults to None.

        *args (Any, optional): The arguments we want to pass to the initializer function

    Returns:
        [bytes]: Return the encoded function bytes.
    """
    # If there is no args or not havaing initalizer then reurn empty hex string
    if len(args) == 0 or not initalizer:
        return eth_utils.to_bytes(hexstr="0x")

    # Encoding this into bytes so that our sc knows what function to call
    return initalizer.encode_input(*args)


def upgrade(
    account,
    proxy_contract,
    new_implementation_contract,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    tx = None
    if proxy_admin_contract:
        if initializer:
            # Getting encoded initializer function
            encoded_initializer = encode_fun_data(initializer, *args)
            # upgradeAndCall for passing the initializer if not having initializer function in new contract then use upgrade only for best practices
            tx = proxy_admin_contract.upgradeAndCall(
                proxy_contract.address,
                new_implementation_contract.address,
                encoded_initializer,
                {"from": account, "gas": 1000000},
            )
        else:
            tx = proxy_admin_contract.upgrade(
                proxy_contract.address,
                new_implementation_contract.address,
                {"from": account, "gas": 1000000},
            )
    else:  # If not the admin then no need to call admin functions only direcly call proxy_contract function so there is no confusion
        if initializer:
            # Getting encoded initializer function
            encoded_initializer = encode_fun_data(initializer, *args)
            # upgradeAndCall for passing the initializer if not having initializer function in new contract then use upgrade only for best practices
            tx = proxy_contract.upgradeToAndCall(
                new_implementation_contract.address,
                encoded_initializer,
                {"from": account, "gas": 1000000},
            )
        else:
            tx = proxy_contract.upgradeTo(
                new_implementation_contract.address,
                {"from": account, "gas": 1000000},
            )
    return tx
