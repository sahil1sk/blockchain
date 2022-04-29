from web3 import Web3
from scripts.helper import get_account
from brownie import DappToken, TokenFarm, network, config


KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_farm_and_dapp_token():
    account = get_account()
    dapp_token = DappToken.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # We send all the balance to the token farm contract to give rewards dapp tokens and only remained 100 balance from DAPP TOKEN
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)

    weth_token_address = config["networks"][network.show_active()]["weth_token"]
    fau_token_address = config["networks"][network.show_active()]["fau_token"]
    # We are setting the price feeds for the tokens
    # for dapp and fau we gave dai to usd price feed means (dapp and fau price equal to dia token)
    # for weth we gave eth to usd price feed means (weth price equal to eth token)
    dict_of_allowed_tokens = {
        dapp_token.address: config["networks"][network.show_active()][
            "dai_usd_price_feed"
        ],
        fau_token_address: config["networks"][network.show_active()][
            "dai_usd_price_feed"
        ],
        weth_token_address: config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ],
    }
    # dapp_token, weth_token, fau_token/dia
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        # Adding tokens address to the list of allowed tokens
        add_tx = token_farm.addAllowedTokens(token, {"from": account})
        add_tx.wait(1)
        # Setting the price feed for the token and it's address from where we get this price of the token
        set_tx = token_farm.setPriceFeedContract(
            token, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)
    return token_farm


def main():
    deploy_token_farm_and_dapp_token()
