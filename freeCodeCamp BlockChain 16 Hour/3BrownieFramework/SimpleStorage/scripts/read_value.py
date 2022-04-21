from brownie import SimpleStorage, accounts, config


def read_contract():
    # SimpleStorage[] contians all the deployments and at last latest deployment so -1 index will give latest deployment
    # So in this way we are able to interact with the latest deployment
    ss = SimpleStorage[-1]
    ss.retrieve()


def main():
    read_contract()
