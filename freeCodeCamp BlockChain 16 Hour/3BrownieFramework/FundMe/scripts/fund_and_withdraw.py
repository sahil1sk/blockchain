import imp
from brownie import FundMe
from scripts.helper import get_account


def fund():
    fm = FundMe[-1]
    account = get_account()
    enterance_fee = fm.getEntranceFee()  # Getting enterance fee to fund
    print(f"The current entry free is {enterance_fee}")
    print("Funding")
    # for send the value to payable methods using value
    fm.fund({"from": account, "value": enterance_fee})


def withdraw():
    fm = FundMe[-1]
    account = get_account()
    print("Withdrawing")
    fm.withDraw({"from": account})


def main():
    fund()
    withdraw()
