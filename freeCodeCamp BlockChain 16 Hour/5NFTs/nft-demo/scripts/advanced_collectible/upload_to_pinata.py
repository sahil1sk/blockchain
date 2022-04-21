###### INSTEAD IPFS you can also use Pinata to upload the files in decentralized way ########

import os
from pathlib import Path
import requests

PINATA_BASE_URL = "https://api.pinata.cloud"
endpint = "/pinning/pinFileToIPFS"


# Change this filepath
filepath = "./img/pug.png"
filename = filepath.split("/")[-1:][0]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}


# upload_to_ipfs
# We can alos use pinata server to upload our images decentralized way


def main():
    with Path(filepath).open("rb") as f:
        image_binary = f.read()
        response = requests.post(
            PINATA_BASE_URL + endpint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print("https://gateway.pinata.cloud/ipfs/" + response.json()["IpfsHash"])
