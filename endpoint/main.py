import time

import requests
from ergpy import helper_functions, appkit

# Create connection to the blockchain
node_url: str = "http://213.239.193.208:9052/"  # MainNet or TestNet
ergo = appkit.ErgoAppKit(node_url=node_url)
wallet_mnemonic = "gate swing banana royal feed pudding aim grow typical secret keep cabin curve pitch bus"


def block():
    try:
        URL = f'{node_url}info'
        return requests.get(URL).json()['fullHeight']
    except Exception as e:
        time.sleep(30)
        URL = f'{node_url}info'
        return requests.get(URL).json()['fullHeight']


def blockTime(block):
    URL = f'{node_url}info'
    height = requests.get(URL).json()['fullHeight']
    if height == block:
        return height
    elif block < height:
        return height
    time.sleep(10)
    return blockTime(block)


def blockHeight(block):
    blockTime(block)
    return True


def getERG(receiver_address):
    blockHeight(block() + 1)
    return helper_functions.simple_send(ergo=ergo, amount=[0.01], wallet_mnemonic=wallet_mnemonic,
                                        receiver_addresses=[receiver_address])


def exit():
    helper_functions.exit()
