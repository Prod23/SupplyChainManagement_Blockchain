class SupplyChainBlockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.create_block("0",genesis_block= True)
        self.participants = {}
        self.deliveries_in_progress = {}
        self.disputes = []
        self.votes=[]

    def participant(self, name, type_,id, amount):
            self.participants[name] = { "type": type_, "amount": amount, "products": [] }
            if type_ == "distributor":
              # print(id[1])
              # index=int(id[1])
              self.votes.append({id:0})
              # print(id[1])

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
            'merkle_root': self.get_merkle_root(self.current_transactions),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block



    def add_transaction(self, manufacturer, distributor, client, product, amount):
        self.current_transactions.append({
            'manufacturer': manufacturer,
            'distributor': distributor,
            'client': client,
            'product': product,
            'amount': amount,
            'timestamps': {"received_by_distributor": time.time(), "dispatched": time.time(), "received_by_client": time.time()}
        })
        return self.last_block['index'] + 1

    def get_merkle_root(self, transactions):
      mt=MerkleTree()
      return mt.get_merkle_root()


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
        display(Image(filename=file_path))



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



    def dpos_consensus(self):
      validators = [node for node in self.nodes if self.participants[node]['type'] == 'distributor']
      if not validators:
          raise ValueError("No validators available. Register a distributor node before creating a block.")
      selected_validator = random.choice(validators)
      return selected_validator


    @staticmethod
    def hash(block):
        transactions = block['transactions']
        transactions.append(block['previous_hash'])
        print(transactions)
        mt = MerkleTree()
        for transaction in transactions:
            mt.add_leaf(transaction)
        mt.make_tree()
        return mt.get_merkle_root()

    @property
    def last_block(self):
        return self.chain[-1]
