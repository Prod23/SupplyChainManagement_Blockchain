import hashlib
from sys import displayhook
import time
import json
import random
from tkinter import Image
import qrcode
from merkleTree import MerkleTree


class SupplyChainBlockchain:
    def __init__(self):
        self.chain = [] 
        self.unverified_transactions = []
        self.current_transactions = []
        self.transaction_history = dict()
        
        self.chain=[] #to store the chain

        self.create_block("0",genesis_block= True) #genesis block, contains no transactions
        
        self.participants = dict()
        
        self.deliveries_in_progress = {}
        
        self.disputes = []
        
        self.votes=[]

        self.delegates=dict()

        self.stakers=dict()

        self.witnesses=dict()

    # def add_users(self,participants):
    #     self.participants.update(participants)
    #     print(self.participants)


    def participant(self, participants):
            # self.participants[name] = { "type": type_, "amount": amount, "products": [] }
            # if type_ == "distributor":
            #   # print(id[1])
            #   # index=int(id[1])
            #   self.votes.append({id:0})
              # print(id[1])
        self.participants.update(participants)
        print(self.participants)

    def add_staker(self,stakers):
        self.stakers.update(stakers)


    def create_block(self, previous_hash=None,genesis_block=False):
        
        if not genesis_block:
          validator = self.dpos_consensus()  # Decide who gets to create the block
        else:
          validator=None
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'validator': validator,  # The entity who added the block
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'merkle_root': self.generate_merkle_root(self.current_transactions),
        }

        self.current_transactions = []
        self.deliveries_in_progress=[]
        self.chain.append(block)
        self.unverified_transactions=[]
        return block
    
    
    def confirm_transactions(self):
        last_block = self.last_block
        transactions = last_block['transactions']

        for tx in transactions:
            d = tx['distributor']
            c = tx['client']

            if d in self.deliveries_in_progress and self.deliveries_in_progress[d] == c:
                self.confirm_delivery(d, c)
                
    def confirm_deivery(self,distributor, client):
        self.deliveries_in_progress.pop(distributor,None)

    def generate_merkle_root(self, transactions):
        mt = MerkleTree()
        
        for tx in transactions:
            tx_string = json.dumps(tx, sort_keys=True) 
            tx_hex = tx_string.encode('utf-8').hex()
            mt.add_leaf(tx_hex)  
            
        mt.make_tree() 
        return mt.generate_merkle_root()  
    

    def dpos_consensus(self):
        validators = list(self.witnesses.keys())
        selected_validator = random.choice(validators)# For illustration purposes
        return selected_validator
    
   

    def add_transaction(self, manufacturer, distributor, client, product, amount):
        self.current_transactions.append({
            'manufacturer': manufacturer,
            'distributor': distributor,
            'client': client,
            'product': product,
            'amount': amount,
            'timestamps': {"received_by_distributor": time.time(), "dispatched": time.time(), "received_by_client": time.time()}
        })

        self.unverified_transactions.append(self.current_transactions)
        return self.last_block['index'] + 1



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
        img.save(file_path)  # Save the QR code as an image file

        # Display
        displayhook(Image(filename=file_path))



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
      return liar



    def dpos_vote(self):
        self.stakers = self.participants
        for participant, _ in self.stakers.items():
            self.delegates[participant] = 0
        for _, value in self.stakers.items():
            candidate,_ = random.choice(list(self.stakers.items()))
            length = len(value['property']) if 'property' in value else 0

            x = length*random.randint(0, length)
            self.delegates[candidate] += x  

    def dpos_result(self):
        print(self.delegates)
        self.delegates = dict(sorted(self.delegates.items(), key = lambda kv: (kv[1], kv[0]), reverse=True))

        self.witnesses = dict(list(self.delegates.items())[0:3])
        print(self.witnesses)


    @staticmethod
    def hash(block):
            transactions = block['transactions']
            transactions.append(block['previous_hash'])
            print(transactions)
            mt = MerkleTree()
            for transaction in transactions:
                mt.add_leaf(transaction)
            mt.make_tree()
            return mt.generate_merkle_root()

    @property
    def last_block(self):
        return self.chain[-1]
