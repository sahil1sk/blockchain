import time
from brownie import network
import pytest  # pip install pytest
from scripts.deploy import deploy
from scripts.helper import (
    FORKED_LOCAL_ENVS,
    LOCAL_BLOCKCHAIN_ENVS,
    get_account,
    fund_with_link,
)


# Sometime gas estimation failed because it works in real world
def test_integration():
    if (network.show_active() in FORKED_LOCAL_ENVS) or (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVS
    ):
        pytest.skip("You are not on real network")
    lottery = deploy()
    account = get_account()
    value = lottery.getEnteranceFee()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": value})
    lottery.enter({"from": account, "value": value})

    # fund_with_link(lottery.address)           # Actually to fund to link contract if we are getting random number from link contract but we use another way there
    lottery.endLottery({"from": account})
    time.sleep(5)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
