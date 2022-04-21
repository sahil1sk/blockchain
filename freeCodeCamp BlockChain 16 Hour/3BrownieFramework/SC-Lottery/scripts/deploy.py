from brownie import Lottery, config, network
from scripts.helper import get_account, get_contract, fund_with_link
import time

# /*
#     Search Like Aggregator Contract addreses chainlink docs

#     // These all are different according to networks like for Rinkeby, Mainnet others are there
#     // You will get all these addresses from chainlink docs

#     // You will get this address from chainlink docs AggregatorV3Interface according to the network you want
#     address _priceFeedAddress,

#     // You will get this address from chainlink docs Link Token Contracts
#     address _link,


#     // You will get this address from chainlink docs VRFConsumerBase according to the network you want
#     address _vrfCordinator,
#     uint256 _fee,
#     bytes32 _keyhash
# */
def deploy():
    account = get_account()
    # deploy act like Lottery constructor passing all constructor arguments and account and publish source
    # publish_source verify means verify this contract by our key which we provided in env and the push on ether network so then we will get Green tick on our contract and UI
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Lottery contract address: {lottery.address}")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("Lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEnteranceFee()
    # Passing payable ehtereum value
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


# only works on real network
def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # Fund the contract  (To Link contract to get random number from the outside the ethereum world)
    # Then end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)

    # We sleep here as we know in endLottery function we call requestRandomness which will in return call other function to give us random number back
    # so this process takes time so for some seconds we slept our fuction here and then fetch the recent winner
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy()
    # start_lottery()
    # enter_lottery()
    # end_lottery()
