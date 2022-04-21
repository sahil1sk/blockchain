from brownie import network, exceptions
import pytest  # pip install pytest
from scripts.deploy import deploy
from scripts.helper import FORKED_LOCAL_ENVS, get_account, fund_with_link
from web3 import Web3


def test_get_enterance_fee():
    if network.show_active() not in FORKED_LOCAL_ENVS:
        pytest.skip("You are not in forked network")
    lottery = deploy()
    enterance_fee = lottery.getEnteranceFee()
    expected_fee = Web3.toWei(0.0072, "ether")  # More than 20 Dollar ether
    assert enterance_fee < expected_fee


def test_cant_enter_unless_started():
    if network.show_active() not in FORKED_LOCAL_ENVS:
        pytest.skip("You are not in forked network")
    lottery = deploy()

    # Act as assert (Because lottery is not started yet and we try to enter so except an error)
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEnteranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in FORKED_LOCAL_ENVS:
        pytest.skip("You are not in forked network")
    lottery = deploy()
    enterance_fee = lottery.getEnteranceFee()
    account = get_account()
    lottery.startLottery({"from": account})
    # Action
    lottery.enter({"from": account, "value": enterance_fee})
    # Assert
    assert lottery.players(0) == account


# only works on real network
def test_can_end_lottery():
    # Arrange
    if network.show_active() not in FORKED_LOCAL_ENVS:
        pytest.skip("You are not in forked network")
    lottery = deploy()
    enterance_fee = lottery.getEnteranceFee()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": enterance_fee})
    # Action
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})
    # Assert
    assert lottery.lotteryState() == 2


def test_can_pick_winner_correctly():
    # Arrange
    if network.show_active() not in FORKED_LOCAL_ENVS:
        pytest.skip("You are not in forked network")
    lottery = deploy()
    enterance_fee = lottery.getEnteranceFee()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": enterance_fee})
    lottery.enter({"from": get_account(index=2), "value": enterance_fee})
    lottery.enter({"from": get_account(index=3), "value": enterance_fee})
    # Action
    fund_with_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    # tx.events containing all the elements
    request_id = tx.events["RequestedRandomness"]["requestId"]
    ## Related to Mocks so we are not able to do because of LinkToken uncompatible with our latest version
    # Basically here we are calling mock function of vrf to send back the response with the random number
    # STATIC_RNG = 777
    # get_contract("vrf_coordinator").callBackWithRandomness(
    #     request_id, STATIC_RNG, lottery.address, {"from", account}
    # )

    starting_balance = account.balance()
    lottery_balance = lottery.balance()
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance + lottery_balance
