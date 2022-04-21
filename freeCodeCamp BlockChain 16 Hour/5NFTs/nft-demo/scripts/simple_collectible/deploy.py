from brownie import SimpleCollectible
from scripts.helper import get_account, OPENSEA_URL

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy():
    account = get_account()
    sc = SimpleCollectible.deploy({"from": account})
    tx = sc.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(sc.address, sc.tokenCounter() - 1)}"
    )
    return sc


def main():
    deploy()
