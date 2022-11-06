from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from web3 import Web3
import asyncio
import wrappers as Wrap
import os
from time import sleep
from spawner import vast_spawner, gcloud_spawner
from multiprocessing import Process

WALLET_KEY = "0x2a563faFcbEd3D3E85C555B9B33C9C54e601BF8F"

CREATE_NODE = False
SERVE_NODE = True

INFURA_URL = "https://withered-fittest-daylight.ethereum-goerli.discover.quiknode.pro/c758af9653c412cb3afe3308f6741e2d49f172bd/"
SC_ADDRESS = "0x27E9678557070faa7183EDB137BEA1BF94090cA8"

ABI_PATH = "TorpedoFactory.json"
TS_ABI_PATH = "TorpedoSession.json"
# Event Handler Class
w3 = Web3(
    Web3.HTTPProvider(
        "https://withered-fittest-daylight.ethereum-goerli.discover.quiknode.pro/c758af9653c412cb3afe3308f6741e2d49f172bd/"
    )
)


class Handler:
    def __init__(self, IP = None, port = None, sshKey = None) -> None:

        self.gpu_type = 1        
        # Establish connection to the blockchain node
        self.web3 = Web3(Web3.HTTPProvider(INFURA_URL))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Connect to all smart contracts
        self.SC = self.web3.eth.contract(
            address=SC_ADDRESS, abi=json.load(open(ABI_PATH))["abi"]
        )
        # initialise node data onto the smart contract

    def create_node(self,gpu_type=1):
        # function = self.SC.functions.createNode(**self._jupyter)# add SSH info here
        self.gpu_type = gpu_type
        time_stamp = self.SC.functions.getNow().call()
        time_code = time_stamp + 3600 * 50
        function = self.SC.functions.registerPhaestus(2, 2, time_code, 1, self.gpu_type, 2, 32, 16)
        Wrap.wrap_transact(self.web3, function)

        # self._get_nodeId()

    def _handle_event(self, event):
        data = json.loads(Web3.toJSON(event))["args"]
        self._nodeId = data["_nodeId"]
        print("Node ID: " + str(self._nodeId))
        return True

    def _secureClient(self, event):
        data = json.loads(Web3.toJSON(event))["args"]
        self._clientId = data["_clientId"]
        # sending client id - 1 due to stupid bug...fix later...
        function = self.SC.functions.claimClient(int(self._clientId))
        sleep(3)
        Wrap.wrap_transact(self.web3, function)
        print("Client ID: " + str(self._clientId))
        return True

    async def _log_loop(self, event_filter, poll_interval, _type="init"):
        check = False
        while not check:
            for event in event_filter.get_new_entries():
                if _type == "init":
                    check = self._handle_event(event)
                elif _type == "client":
                    check = self._secureClient(event)
            await asyncio.sleep(poll_interval)

    def _get_nodeId(self):
        event_filter = self.SC.events.PhaestusNodeCreated.createFilter(
            fromBlock="latest"
        )
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(self._log_loop(event_filter, 2, _type="init"))
            )
        finally:
            loop.close()

    def secureClient(self):
        event_filter = self.SC.events.checkStatusOfPhaestus.createFilter(
            fromBlock="latest"
        )
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(self._log_loop(event_filter, 1, _type="client"))
            )
        finally:
            loop.close()

    def check_for_phaestus(self):
        
        phaestus_activated = False
        while not phaestus_activated:
            phaestus_activated, TS_ADDRESS = self.SC.functions.phaestusToActivate(
                WALLET_KEY
            ).call()
            sleep(1)
            print(phaestus_activated)
        
        print(TS_ADDRESS)
        #CLIENT_WALLET_ADDRESS = self.SC.functions.getClientAddress().call()
        #print(CLIENT_WALLET_ADDRESS)
        #AFTER NAP: GET SPAWNING WORKING PERFECTLY WITH GCLOUD AND VAST
        # subroutine: send payload
        self.TS_SC = self.web3.eth.contract(
            address=TS_ADDRESS, abi=json.load(open(TS_ABI_PATH))["abi"]
        )
        #print(self.TS_SC.getSessionRequest())

        if self.gpu_type == 1:
            payload = vast_spawner()
        else:
            payload = gcloud_spawner()
            
        
            
        send_payload = self.TS_SC.functions.initialiseSession(payload, "0")

        Wrap.wrap_transact(self.web3, send_payload)

        # print(self.SC.functions.getClientAddress().call())
        os.chdir("cli-starter")
        os.system(
            "./xmtp send 0xA8B867adB1bDaEE36427bc4AC5F573dd2fe9F0E3 {payload}".format(
                payload=payload
            )
        )
    

if __name__ == "__main__":
    
    phaestus_vast = Handler()
    
    if CREATE_NODE:
        print("Creating node...")
        phaestus_vast.create_node(gpu_type=1)
    else:
        print("Skipping node creation...")
    
    print("Your node has successfully registered on the torpedo smart contract!")
    print("Looking for clients...")
    while SERVE_NODE:
        phaestus_vast.check_for_phaestus()
    #sleep(10)

