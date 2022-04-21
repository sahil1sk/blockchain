from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    # LinkToken,
    Contract,
    interface,
)

FORKED_LOCAL_ENVS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local"]

DECIMALS = 8  # So sending decimal will be 8
STARTING_PRICE = 200000000000  # Decimal is 8 so that's why adding extra 8 zeros


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(
            id
        )  # Loading account which we added in env account by account create command

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVS
        or network.show_active() in FORKED_LOCAL_ENVS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


# To access dict in . that's why we make this class
class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


#### OUR NORMAL MOCKS NOT WORKING BECAUSE OF LINK TOKEN MOCK WAS IN 4.0 VERSION WHICH IS NOT COMPATIBALE
#### BUT OUR FORKS NETWORKS ARE WORKING FINES SO TEST THERE

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    # "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brwnie config
    if defined, otherwise, it will deploy a mock version of that contract and
    return that mock contract.

        Args:
            contract_name(string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract
    """
    # contract_type = contract_to_mock[contract_name]  # like MockV3Aggregator
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS:
        contract_type = contract_to_mock[contract_name]  # like MockV3Aggregator
        if len(contract_type) <= 0:  # like MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]  # like MockV3Aggregator[-1]
    else:  # Else if we are on mainnet or forked mainnet then get the address from our brownie config
        contract_address = config["networks"][network.show_active()][contract_name]
        # To get Contract address and abi
        # contract = Contract.from_abi(
        #     contract_type.name, contract_address, contract_type.abi
        # )
        contract = dotdict({"address": contract_address})

    return contract


# Deploying Aggregator Mock (Which we used for price feed)
def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, starting_price, {"from": account})
    # lt = LinkToken.deploy({"from": account})
    # VRFCoordinatorMock.deploy(lt.address, {"from": account})
    print("Deployed")


def fund_with_link(  # 0.25 Link
    contract_address, account=None, link_token=None, amount=250000000000000000
):
    # If the send the account then take that one otherwise regular get_account
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # You will get the contract by searching the link token interface
    # By using interface and address you are able to get the address
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    # Transferring the money to contract of Link Token to generating the Random number for the contract address which we pass
    tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    # If you have contract then direct do transfer no need to use interface
    tx.wait(1)
    print("Contract Funded!")
    return tx
