from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helper import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVS


def deploy():
    account = get_account()

    # If we are on a persistent network like rinkeby, use the associated address
    # otherwise deploy mocks (means fake for local ganache)

    # If it is development mode or our ganache-local then we will deploy our Mock chainlink interface for testing purpose which will help to get the price feed data
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pf_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        # -1 means always pick latest deployed address -1 is last index
        pf_address = MockV3Aggregator[-1].address

    fm = FundMe.deploy(  # Passing address
        pf_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # verify true means our (when we get our contract by using it's address it will give us check and give interface to interact from web)
    print(fm.address)
    return fm


def main():
    deploy()
