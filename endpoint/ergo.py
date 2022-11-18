import os
import time
import requests
from ergpy import helper_functions, appkit
import SQL_functions
import logging
from dotenv import load_dotenv

load_dotenv()

LOGGING_FORMAT = '[%(asctime)s] - [%(levelname)-8s] -  %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create connection to the blockchain

node_url = os.getenv("NODE_URL")
if node_url[-1] != "/":
    node_url = node_url + "/"
ergo = appkit.ErgoAppKit(node_url=node_url)
wallet_mnemonic = os.getenv("MNEMONIC")

wallet_address = helper_functions.get_wallet_address(ergo=ergo, amount=1, wallet_mnemonic=wallet_mnemonic)

genesis_tx = helper_functions.simple_send(ergo=ergo, amount=[10000], wallet_mnemonic=wallet_mnemonic,
                                          receiver_addresses=wallet_address,
                                          return_signed=True)
genesis_outbox = appkit.get_outputs_to_spend(genesis_tx, 0)
ergo.txId(genesis_tx)
outBox_list = []
tx_1 = helper_functions.simple_send(ergo=ergo, amount=[0.1], wallet_mnemonic=wallet_mnemonic,
                                    receiver_addresses=wallet_address,
                                    input_box=genesis_outbox,
                                    return_signed=True, chained=True)
tx_1_outbox = appkit.get_outputs_to_spend(tx_1, 0)
outBox_list.append(tx_1_outbox)
ergo.txId(tx_1)


def block():
    try:
        URL = f'{node_url}info'
        return requests.get(URL).json()['fullHeight']
    except Exception as e:
        time.sleep(30)
        URL = f'{node_url}info'
        return requests.get(URL).json()['fullHeight']


def address_validity(address):
    try:
        URL = f'{node_url}utils/address/{address}'
        return bool(requests.get(URL).json()['isValid'])
    except Exception as e:
        time.sleep(30)
        URL = f'{node_url}utils/address/{address}'
        return bool(requests.get(URL).json()['isValid'])


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


def getERG(receiver_address, uuid):
    while True:
        try:
            tx = helper_functions.simple_send(ergo=ergo, amount=[10], wallet_mnemonic=wallet_mnemonic,
                                              receiver_addresses=[receiver_address],
                                              input_box=outBox_list[len(outBox_list) - 1],
                                              return_signed=True, chained=True)
            tx_outbox = appkit.get_outputs_to_spend(tx, 0)
            outBox_list.append(tx_outbox)
            txid = ergo.txId(tx)
            SQL_functions.write_to_faucet_table("faucet", "faucet", str(uuid), str(txid))
            break
        except Exception as e:
            logging.critical(e)
            outBox_list.clear()
            genesis_tx = helper_functions.simple_send(ergo=ergo, amount=[5000], wallet_mnemonic=wallet_mnemonic,
                                                      receiver_addresses=wallet_address,
                                                      return_signed=True)
            genesis_outbox = appkit.get_outputs_to_spend(genesis_tx, 0)
            ergo.txId(genesis_tx)
            tx_1 = helper_functions.simple_send(ergo=ergo, amount=[0.1], wallet_mnemonic=wallet_mnemonic,
                                                receiver_addresses=wallet_address,
                                                input_box=genesis_outbox,
                                                return_signed=True, chained=True)
            tx_1_outbox = appkit.get_outputs_to_spend(tx_1, 0)
            outBox_list.append(tx_1_outbox)
            ergo.txId(tx_1)


def exit():
    helper_functions.exit()
