import datetime
import json
import os

from dotenv import load_dotenv
from eth_account.datastructures import SignedTransaction
from eth_account.signers.local import LocalAccount
from web3 import Web3

from app.DTO.Audit import ActionDTO
from app.ext.extensions import db
from app.models import AuditLog

load_dotenv()


class MyWeb3Client:

    def __init__(self):
        self.PRIVATE_KEY = os.getenv('PRIVATE_KEY')
        self.CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv('CONTRACT_ADDRESS'))
        self.RPC_URL = os.getenv('RPC_URL')
        self.w3 = Web3(Web3.HTTPProvider(self.RPC_URL))
        self.account: LocalAccount = self.w3.eth.account.from_key(self.PRIVATE_KEY)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(base_dir,'OperationLogger.json')
        with open(json_file_path, 'r') as f:
            contract_data = json.load(f)
            self.CONTRACT_ABI = contract_data['abi']
        self.contract = self.w3.eth.contract(address=self.CONTRACT_ADDRESS, abi=self.CONTRACT_ABI)

    def syncToBlockChain(self, actionDTO: ActionDTO):
        try:

            txn = self.contract.functions.logOperation(actionDTO.model_dump_json()).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gasPrice': self.w3.eth.gas_price
            })
            estimated_gas = self.w3.eth.estimate_gas(txn)
            txn['gas'] = int(estimated_gas * 1.2)  # 加 20% 作为缓冲以防止 Gas 不足
            signed_txn: SignedTransaction = self.w3.eth.account.sign_transaction(txn, self.PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            log_entry = AuditLog(user_id=actionDTO.userId,
                                 action=actionDTO.model_dump(),
                                 timestamp=datetime.datetime.now(),
                                 blockchain_tx_hash=tx_hash.hex(),
                                 blockchain_block_number=tx_receipt['blockNumber'],
                                 blockchain_operator=self.account.address)
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            raise e

# 单例模式
myWeb3Client = MyWeb3Client()
