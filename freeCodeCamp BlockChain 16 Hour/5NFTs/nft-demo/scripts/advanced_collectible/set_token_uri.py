from brownie import network, AdvanceCollectible
from scripts.helper import OPENSEA_URL, get_account, get_breed

# We will get this uri directly from our create_metadata fuction
dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"Working on {network.show_active()}")
    ac = AdvanceCollectible[-1]
    print(f"Constract address on {network.show_active()} network is: {ac.address}")
    number_of_ac = ac.tokenCounter()
    print(f"Number of AdvanceCollectibles: {number_of_ac}")

    for token_id in range(number_of_ac):
        # You can get the breead from our stored mappings
        breed = get_breed(ac.tokenIdToBreed(token_id))
        # You are able to access tokenURI using ID available in the contract by ERC721
        if not ac.tokenURI(token_id).startswith("https://"):
            set_tokenURI(token_id, ac, dog_metadata_dic[breed])
        else:
            print(
                f"Awesome! You can view your NFT at {OPENSEA_URL.format(ac.address, token_id)}"
            )
            print("MetaData URI: ", ac.tokenURI(token_id))


def set_tokenURI(token_id, ac_contract, tokenURI):
    account = get_account()
    # Setting Metadata token uri
    tx = ac_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(ac_contract.address, token_id)}"
    )
    print(
        "Please wait up to 20 minutes, and hit the refresh metadata button on the your NFT (Refresh button given with Share on NFT image)"
    )
