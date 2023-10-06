
#Importing libraries.
import hashlib
from datetime import datetime
import json
import random
import qrcode
from merkleTree import MerkleTree
from crypto.Signature import pkcs1_15
from crypto.Hash import SHA256
from crypto.PublicKey import RSA






class SupplyChainBlockchain:
    def __init__(self):
        self.nonce = random.randint(100,999)
        self.chain = []
        self.unverified_transactions = []
        self.current_transactions = []
        self.transaction_history = dict()
        self.chain = []
        self.create_genesis_block(genesis_block=True)
        self.participants = dict()  # Define participants attribute here
        self.deliveries_in_progress = {}
        self.disputes = []
        self.votes = []
        self.digitalSignature = False  # Flag to indicate digital signature status
        self.delegates = dict()
        self.stakers = dict()
        self.witnesses = dict()

    # Initialize participants
    def participant(self, participants):
        
        self.participants.update(participants)

    def generate_signature(self,private_key, message):
        key = RSA.import_key(private_key)
        h = SHA256.new(message.encode())
        signature = pkcs1_15.new(key).sign(h)
        return signature.hex()
    
    def verify_signature(self,public_key, message, signature):
        key = RSA.import_key(public_key)
        h = SHA256.new(message.encode())
        try:
            pkcs1_15.new(key).verify(h, bytes.fromhex(signature))
            return True
        except (ValueError, TypeError):
            return False
    
    # You'll have to modify the logic here based on your QR scanning implementation
    def confirm_receipt(self,transaction_data, distributor_public_key):
        signature = transaction_data.get("signature")
        if not signature:
            return False
        data_without_signature = {key: val for key, val in transaction_data.items() if key != "signature"}
        return self.verify_signature(distributor_public_key, json.dumps(data_without_signature), signature)


    # Add stakers
    def add_staker(self, stakers):
        self.stakers.update(stakers)

    # Create a genesis block for the blockchain
    def create_genesis_block(self, genesis_block=True):
        if genesis_block:
            p_hash = hashlib.sha256(datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode()).hexdigest()
            m_root = hashlib.sha256("genesis".encode()).hexdigest()
            block = {
                'index': len(self.chain),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'transactions': None,
                'previous_hash': p_hash,
                'merkle_root': m_root,
                'nonce':self.nonce
                
            }

            self.chain.append(block)
            return block

    # Create a new block in the blockchain
    def create_block(self, previous_hash=None, genesis_block=False):
        if not genesis_block:
            validator = self.dpos_consensus()
        else:
            validator = None
        block = {
            'index': len(self.chain) ,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': self.current_transactions,
            'validator': validator,
            'previous_hash': self.prev_hash(self.chain[-1]),
            'merkle_root': self.generate_merkle_root(self.current_transactions),
            'nonce':self.nonce
        }
        self.current_transactions = []
        self.deliveries_in_progress = {}
        self.chain.append(block)
        self.unverified_transactions = []
        return block

    # Confirm transactions in the blockchain
    def confirm_transactions(self):
        last_block = self.last_block
        transactions = last_block['transactions']
        for tx in transactions:
            d = tx['distributor']
            c = tx['client']
            if d in self.deliveries_in_progress and self.deliveries_in_progress[d] == c:
                self.confirm_delivery(d, c)

    # Confirm delivery of a product
    def confirm_delivery(self, distributor, client):
        self.deliveries_in_progress.pop(distributor, None)

    # Generate the Merkle root of transactions
    def generate_merkle_root(self, transactions):
        mt = MerkleTree()
        for tx in transactions:
            tx_string = json.dumps(tx, sort_keys=True)
            tx_hex = tx_string.encode('utf-8').hex()
            mt.add_leaf(tx_hex)
        mt.make_tree()
        return mt.generate_merkle_root()

    # Implement DPoS consensus mechanism
    def dpos_consensus(self):
        validators = list(self.witnesses.keys())
        selected_validator = random.choice(validators)
        return selected_validator

    # Add a new transaction to the blockchain
    def add_transaction(self, manufacturer, distributor, client, product, amount):
        self.digitalSignature = False  # Reset digital signature flag
        manufacturer_to_distributor = {
            'manufacturer': manufacturer,
            'distributor': distributor,
            'product': product,
            'amount': amount,
            'timestamps': {
                "sent_by_manufacturer": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "received_by_distributor": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        }
        distributor_to_client = {
            'distributor': distributor,
            'client': client,
            'product': product,
            'amount': amount,
            'timestamps': {
                "received_by_distributor": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "dispatched": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "received_by_client": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        }
        if client=="": 
            self.current_transactions.append(manufacturer_to_distributor)
        else : 
            self.current_transactions.append(distributor_to_client)
        self.nonce = random.randint(100,999)
        self.unverified_transactions.append(self.current_transactions)
        return self.last_block['index'] + 1

    # Generate a QR code for a transaction
    def generate_qr_code(self, transaction, file_path='qr_code.png'):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(transaction))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)

    # Resolve a dispute and identify the liar
    def resolve_dispute(self, dispute):
        liar = None
        client_id = dispute['client_id']
        distributor_id = dispute['distributor_id']
        if dispute['client_claim'] != dispute['distributor_claim']:
            if dispute['client_claim'] is False:
                liar = client_id
            else:
                liar = distributor_id
            self.entities[liar]['amount'] -= dispute['penalty']
        return self.digitalSignature  # Return the digital signature flag

    # Implement DPoS voting
    def dpos_vote(self):
        self.stakers = self.participants
        for participant, _ in self.stakers.items():
            self.delegates[participant] = 0
        for _, value in self.stakers.items():
            candidate, _ = random.choice(list(self.stakers.items()))
            length = len(value['property']) if 'property' in value else 0
            x = length * random.randint(0, length)
            self.delegates[candidate] += x

    # Get the result of DPoS consensus
    def dpos_result(self):
        print(self.delegates)
        self.delegates = dict(sorted(self.delegates.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
        self.witnesses = dict(list(self.delegates.items())[0:3])

    # Calculate the Merkle root hash of a block
    @staticmethod
    def hash(block):
        block_string = json.dumps({
            'timestamp': block['timestamp'],
            'previous_hash': block['previous_hash'],
            'merkle_root': block['merkle_root'],
            'nonce': block['nonce']  # Include nonce in the block string for hashing
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # Get the previous block's Merkle root hash
    def prev_hash(self, block):
        return self.hash(block)

    # Get the last block in the blockchain
    @property
    def last_block(self):
        return self.chain[-1]
