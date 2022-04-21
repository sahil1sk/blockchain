from brownie import OurToken
from scripts.helper import get_account
from web3 import Web3

intial_supply = Web3.toWei(1000, "ether")


def main():
    account = get_account()
    our_token = OurToken.deploy(intial_supply, {"from": account})
    print(f"OurToken address: {our_token.address}")
    print(f"OurToken balance: {our_token.balanceOf(account)}")
    print(f"OurToken name: {our_token.name()}")
