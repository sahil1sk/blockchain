from brownie import AdvanceCollectible, config, network
from scripts.helper import get_account, OPENSEA_URL


def deploy():
    account = get_account()
    ac = AdvanceCollectible.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # fund with link if you use VRFConsumer before createCollectible line
    tx = ac.createCollectible({"from": account})
    tx.wait(1)
    print(f"Collectible contract address: {ac.address}")
    return ac, tx


def main():
    deploy()
