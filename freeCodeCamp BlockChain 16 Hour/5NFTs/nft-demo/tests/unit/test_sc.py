from scripts.helper import LOCAL_BLOCKCHAIN_ENVS, FORKED_LOCAL_ENVS, get_account
from brownie import network
import pytest
from scripts.simple_collectible.deploy import deploy


def test_can_create_sc():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVS) and (
        network.show_active() not in FORKED_LOCAL_ENVS
    ):
        pytest.skip("Can only run this test on real or maintestnet")
    sc = deploy()
    assert sc.ownerOf(0) == get_account()
