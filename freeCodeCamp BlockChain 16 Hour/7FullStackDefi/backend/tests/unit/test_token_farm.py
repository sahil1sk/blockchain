from ast import If
import pytest  # pip install pytest
from brownie import network, config, exceptions
from scripts.helper import FORKED_LOCAL_ENVS, get_account
from scripts.deploy import deploy_token_farm_and_dapp_token


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in FORKED_LOCAL_ENVS:
        pytest.skip("Skipping test on network: {}".format(network.show_active()))
    non_owner = get_account(index=1)
    # Here we settled the price feed address
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    price_feed_address = config["networks"][network.show_active()]["dai_usd_price_feed"]
    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address

    with pytest.raises(exceptions.VirtualMachineError):
        # This will raise exception because who deployed this contract only able to call this contract
        tx = token_farm.setPriceFeedContract(
            dapp_token.address,
            price_feed_address,
            {"from": non_owner},
        )


def test_stake_tokens(amount_staked):
    # Arrange
    # if network.show_active() not in FORKED_LOCAL_ENVS:
    #     pytest.skip("Skipping test on network: {}".format(network.show_active()))
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    # So first we are approving the token farm contract to spend the tokens
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    # Then we are staking the tokens
    tx = token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    tx.wait(1)
    # Assert
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokenStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address

    # So we will use this test with others
    return token_farm, dapp_token


# amount_staked (will be automatically fetched from conftest.py during test)
def test_issue_tokens(amount_staked):
    # Arrange
    # if network.show_active() not in FORKED_LOCAL_ENVS:
    #     pytest.skip("Skipping test on network: {}".format(network.show_active()))
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    # To take the balance of the account of Dapp Tokens associated with it
    starting_balance = dapp_token.balanceOf(account.address)
    # Act
    # So we are issuing tokens to all users as rewards how much value of token they have add much that amount reward
    # token_farm.issueToken({"from": account})

    # Assert
    assert dapp_token.balanceOf(account.address) == starting_balance
    # assert dapp_token.balanceOf(account.address) == starting_balance + (add amount in dolars which is staked)
