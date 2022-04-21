import time
from scripts.helper import LOCAL_BLOCKCHAIN_ENVS, FORKED_LOCAL_ENVS, get_account
from brownie import network
import pytest
from scripts.advanced_collectible.deploy import deploy


def test_ac_integration():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVS) or (
        network.show_active() in FORKED_LOCAL_ENVS
    ):
        pytest.skip("Only for integration testing means for mainnet")
    ac, tx = deploy()
    time.sleep(1)
    # In integration we are testing on real network so need of randomnessCallback function
    assert ac.ownerOf(0) == get_account()
