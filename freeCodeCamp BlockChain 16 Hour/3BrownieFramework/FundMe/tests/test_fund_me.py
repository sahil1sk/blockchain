from sklearn import exceptions
from scripts.helper import get_account, LOCAL_BLOCKCHAIN_ENVS
from scripts.deploy import deploy
from brownie import network, exceptions, accounts
import pytest  # pip install pytest


def test_can_fund_and_withdraw():
    # We are not able to set what the exact gas amount for the real transaction that's why we are using for locally now
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip("Only local testing")
    account = get_account()
    fm = deploy()
    enterance_fee = fm.getEntranceFee()
    tx = fm.fund({"from": account, "value": enterance_fee})
    tx.wait(1)
    assert fm.addressToAmountFunded(account.address) == enterance_fee
    tx2 = fm.withDraw({"from": account})
    tx2.wait(1)
    assert fm.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip("Only local testing")
    account = get_account()
    fm = deploy()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fm.withDraw({"from": bad_actor})
    # So here we are saying we will get exceptions because other is calling this method not the owner
