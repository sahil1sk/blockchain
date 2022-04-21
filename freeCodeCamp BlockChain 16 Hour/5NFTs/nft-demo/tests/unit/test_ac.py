from scripts.helper import LOCAL_BLOCKCHAIN_ENVS, FORKED_LOCAL_ENVS, get_account
from brownie import network
import pytest
from scripts.advanced_collectible.deploy import deploy


def test_can_create_ac():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVS) and (
        network.show_active() not in FORKED_LOCAL_ENVS
    ):
        pytest.skip("Can only run this test on real or maintestnet")
    ac, tx = deploy()
    # so in test mode we will fetch requestId event from tx
    # then pass that requestId and random number to callBackWithRandomNess mock function if we are using VRFConsume
    assert ac.ownerOf(0) == get_account()
