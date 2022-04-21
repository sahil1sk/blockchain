from brownie import network, accounts, config, MockV3Aggregator

FORKED_LOCAL_ENVS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local"]

DECIMALS = 8  # So sending decimal will be 8
STARTING_PRICE = 200000000000  # Decimal is 8 so that's why adding extra 8 zeros


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVS
        or network.show_active() in FORKED_LOCAL_ENVS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


# Deploying Aggregator Mock (Which we used for price feed)
def deploy_mocks():
    # So if we already deployed locally this means our MockV3Aggregator is already deployed so we will use already deployed address
    if len(MockV3Aggregator) <= 0:
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks")
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("Mocks Deployed")
    else:
        print("Mock Already Deployed......")
