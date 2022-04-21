from brownie import AdvanceCollectible, config, network
from scripts.helper import get_account, OPENSEA_URL


def main():
    account = get_account()
    ac = AdvanceCollectible[-1]
    # fund with link if you use VRFConsumer before createCollectible line
    tx = ac.createCollectible({"from": account})
    tx.wait(1)
    print(f"Collectible contract address: {ac.address}")
