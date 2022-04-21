from pathlib import Path  # Inbuilt package in python
import requests  # Inbuilt package in python
import json

from brownie import AdvanceCollectible, network

from scripts.helper import get_breed
from metadata.sample_metadata import metadata_template


# META DATA WILL LOOKS LIKE THIS
# sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
# Output
# metadata_template = {
#     "name": "",
#     "description": "",
#     "image": "",
#     "attributes": [{"trait_type": "cutness", "value": 100}],
# }


def main():
    create_metadata()


def create_metadata():
    ac = AdvanceCollectible[-1]
    number_of_ac = ac.tokenCounter()
    print(f"Number of AdvanceCollectibles: {number_of_ac}")
    for token_id in range(number_of_ac):
        breed = get_breed(ac.tokenIdToBreed(token_id))
        # getting metadata file name
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        print(f"Metadata file name: {metadata_file_name}")

        # Checking if the file exists with that name
        if Path(metadata_file_name).exists():
            print(
                f"Metadata file already exists: {metadata_file_name} - Delete it to overwrite"
            )
        else:
            print(f"Creating MetaData file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"Am adorable {breed} pup!"
            # Replace _ with - from breed string
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            print(collectible_metadata)
            with open(metadata_file_name, "w") as f:
                json.dump(collectible_metadata, f, indent=4)

            # Now we are uploadint the meta data file to IPFS
            fileURL = upload_to_ipfs(metadata_file_name)

            with open(f"./metadata/{network.show_active()}/fileURLS.txt", "a") as f:
                f.write(f"{token_id}-{breed}.json : {fileURL}\n")

            return fileURL


# You can also use upload to pinata approach
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as f:
        image_binary = f.read()
        # To use this url run => ipfs daemon (Download ipfs first)
        ipfs_url = "http://127.0.0.1:5001"
        # Endpoint for uploading to IPFS
        endpoint = "/api/v0/add"
        response = requests.post(
            ipfs_url + endpoint,
            files={"file": image_binary},
        )
        ipfs_hash = response.json()["Hash"]
        # "./img/PUG.png" -> "PUG.png" (split from slash remove last element upto first split)
        filename = filepath.split("/")[-1:][0]
        return f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
