import os
import shutil
import yaml  # pip install pyyaml
import json


# Converting our brownie-config.yaml to json and then sending to the frontend folder
def update_front_end():
    # Send the build folder to the frontend folder
    copy_folders_to_front_end("./build", "./front_end/src/chain-info")
    # Sending the front end our config in JSON format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            # brownie_config_json.write(json.dumps(config_dict))
            json.dump(config_dict, brownie_config_json)
    print("Frontend updated")


# Sending build folder to frontend folder
def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)  # If there is folder exists delete
    shutil.copytree(src, dest)  # so here e copying the src folder to destination folder


def main():
    update_front_end()
