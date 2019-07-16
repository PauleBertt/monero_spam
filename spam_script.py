import json
import time

import requests
from requests.auth import HTTPDigestAuth
from random import randrange

url = "http://127.0.0.1:18083/json_rpc"

spent_keys = []
# THRESHOLD amount for the "sweep dust"
# can be adjusted but be careful if set too low you will split your inputs infinitely
min_for_tx = 5 * (10 ** 12)
address = 'empty'

list_known_mined = []


def get_address():
    try:
        headers = {'content-type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_address",
            "params": {
                "account_index": 0,
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers,
                                 auth=HTTPDigestAuth('test', '123456')).json()
        return response["result"]["address"]
    except:
        print("Error address")
        print("Maybe you forgot to start the \"monero-wallet-rpc\" first!")
        exit(0)


def sweep_dust(priority=4):
    try:
        headers = {'content-type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "sweep_all",
            "params": {
                "address": address,
                "priority": priority,
                "unlock_time": 0,
                "below_amount": min_for_tx,
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers,
                                 auth=HTTPDigestAuth('test', '123456')).json()
        print("Dust: " + str(response))
    except IOError:
        print("Error sweep_dust")


def sweep_single(key_image):
    outputs_number = int(randrange(3, 16))
    try:
        headers = {'content-type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "sweep_single",
            "params":
                {
                    "address": address,
                    "key_image": key_image,
                    "priority": 4,
                    "unlock_time": 0,
                    "outputs": outputs_number,
                }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers,
                                 auth=HTTPDigestAuth('test', '123456')).json()
        result = response["result"]
        print(result)
        spent_keys.append(key_image)
    except:
        print("Error sweep single: " + str(response))


def get_unspent_key_images():
    unspent_key_images = []
    try:
        headers = {'content-type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "incoming_transfers",
            "params": {
                "transfer_type": "available",
                "verbose": True,
            },
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers,
                                 auth=HTTPDigestAuth('test', '123456')).json()
        transfers = response["result"]["transfers"]
        for transfer in transfers:
            if not transfer["spent"] and transfer["key_image"] not in spent_keys:
                unspent_key_images.append(transfer["key_image"])
        return unspent_key_images
    except (IOError, KeyError) as exception:
        print("Error largest unspent")
        return unspent_key_images


def spam():
    # just to clean up the wallet if to many inputs were generated
    sweep_dust(1)
    while True:
        sweep_dust()
        key_images = get_unspent_key_images()
        for key_image in key_images:
            print("Swept Single: " + str(key_image))
            sweep_single(key_image)
        print("Sleeping")
        time.sleep(60)
        print("Waky Waky")


if __name__ == '__main__':
    address = get_address()
    print("address: " + address)
    spam()
