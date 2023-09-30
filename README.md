# BITS F452 - Blockchain Technology

Implementation of Delegated Proof of Stake(DPoS) consensus algorithm

## Team Members (Group 10)
<ol>
  <li>Hritik Raj (2020B4AA0980H) </li>
  <li>RishiRaj (2020A7PS2075H) </li>
  <li>Sai Priya ( )</li>
  <li>Yugander (2020B4A72335H )</li>
</ol>
 
## Objective 
This assignment focuses on implementing blockchain for Supply Chain Management. The consensus algorithm used is Delegated Proof of Stake(DPoS).<br>


<h2>Implementation</h2>
<ul>
<li>All the methods are defined in blockchain.py and the API routes in app.py</li>
<li>The DPoS consensus algorithm is defined in blockchain.py file.</li>
<li>The merkle root has been implemented in the merkleTree.py file
</ul>

<h3> API Calling-Methods </h3>
<ul>
<li>/add/user - Adding user or node to the network</li>
<li>/add/transaction - Adding an transaction</li>
<li>/chain - displays the current blockchain of nodes</li >
<li>/users - current nodes in the network</li>
<li>/add/staker - adding a staker</li>
<li>/remove/staker</li>
<li>/witnesses</li>  
<li>/qrcode</li>
<li>/mine</li>
</ul>


## Feature -1 

### Register an entity

API calling begins with adding a user of the format:

``` json
{
    "message": "the following participants have been added",
    "participants": {
        "M1": {
            "amount": 1000,
            "id": "M1",
            "name": "Manufacturer1",
            "type": "Manufacturer"
        },
        "c1": {
            "amount": 1000,
            "id": "C1",
            "name": "Client1",
            "type": "client"
        },
        "c2": {
            "amount": 1000,
            "id": "C2",
            "name": "Client2",
            "type": "client"
        },
        "d1": {
            "amount": 1000,
            "id": "D1",
            "name": "Distributor1",
            "property": [
                "wood",
                "sandlewood"
            ],
            "type": "distributor"
        },
        "d2": {
            "amount": 1000,
            "id": "D2",
            "name": "Distributor2",
            "property": [
                "normal-chair",
                "office-chair"
            ],
            "type": "distributor"
        }
    }
}
```

where there is only one manufacturer for the network, along with multiple distributors and clients as nodes. Each node has to be security deposit of 1000 (amount) to the trusted third party in the network.


## Feature -2 

### DPoS 
The delegated proof of stake Consensus Algorithm has been implemented in the blockchain.py as the following methods
[Dpos_vote()](https://github.com/Prod23/SupplyChainManagement_Blockchain/blob/4bed1b209cee0a5132f135d2b10ed2fa6714a4c6/Blockchain.py#L127)
[Dpos_result()](https://github.com/Prod23/SupplyChainManagement_Blockchain/blob/4bed1b209cee0a5132f135d2b10ed2fa6714a4c6/Blockchain.py#L137C4-L137C27)

<h3>DPoS Implementation</h3>

```python
def dpos_vote(self):
    self.stakers = self.participants

```
This function begins by assigning the self.participants to self.stakers. Participants is a dictionary containing information about participants in the DPoS consensus, and stakers is used to represent the participants who will participate in voting.

```python

    for participant, _ in self.stakers.items():
        self.delegates[participant] = 0

```

Here, it initializes a delegates where each participant is initially assigned a vote count of 0. This dictionary will be used to keep track of how many votes each participant receives.


```python

    for _, value in self.stakers.items():
        candidate, _ = random.choice(list(self.stakers.items()))
        length = len(value['product'])
        x = length * random.randint(0, length)
        self.delegates[candidate] += x


```

This loop goes through each participant (represented by value) in self.stakers. For each participant, it selects a random candidate from the list of participants (including themselves) and calculates a vote count (x) based on the length of the participant's 'product' attribute. The vote count is then added to the selected candidate's vote count in the self.delegates dictionary. This loop effectively distributes votes randomly among the participants.


```python
def dpos_result(self):
    print(self.delegates)
    self.delegates = dict(sorted(self.delegates.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    self.witnesses = dict(list(self.delegates.items())[0:3])
    print(self.witnesses)

```

Here, the code sorts the self.delegates dictionary based on the vote counts in descending order. It converts the sorted dictionary back into a regular dictionary and selects the top three participants (witnesses) with the highest vote counts and stores them in the self.witnesses dictionary. 


``` json
{
    "message": "Voting has been successfull and as follows: ",
    "nodes:": {
        "M1": 4,
        "c1": 0,
        "c2": 0,
        "d1": 2,
        "d2": 1
    }
}

```
## Feature -3

### Merkle Tree

We have implemented Merkle tree in the 
[MerkleTree()](https://github.com/Prod23/SupplyChainManagement_Blockchain/blob/3e0fd692c2e10e97614b03d5c97ffa07bbfcec46/MerkleTree.py#L5C12-L5C12)

Have used **SHA-256** as our hash function. Made use of methods like:
<ul>
  <li>add_leaf</li>
  <li>reset_tree</li>
  <li>calculate_next_level</li>
  <li>generate-merkle-root</li>
</ul>


### Mining the Block

<img width="800px" alt="image" src="https://github.com/Prod23/SupplyChainManagement_Blockchain/assets/73677045/440738fa-ff6e-48bf-aa4d-088317554d5f">




## Feature -4 

### QR-Code
A QR for the same has been implemented when scanned tells about the product status of the current transaction.

``` 
http://localhost:5001/qrcode
```
This generates the qrcode giving us the status of the transaction. Here's a sample qrcode generated.

<img  src="./Images/qr_code.png" width = 134px height = 134px>

Generates the following message when scanned:
``` 
{
    'manufacturer': 'Manufacturer1',
    'distributor': 'd2',
    'client': 'Client1',
    'product': 'normal-chair',
    'amount': 550,
    'timestamps':
          {
              'received_by_distributor': '2023-09-30 17:33:04',
              'dispatched': '2023-09-30 17:33:04',
              'received_by_client': '2023-09-30 17:33:04'
          }
}

```





## Feature -5 

### Preventing Double Spending
At one time, the distributor can distribute a product to a dedicated client. Once
the transaction is confirmed by both the distributor and the consumer, then only
the next delivery can be taken by him/her.

<img width="920" alt="image" src="https://github.com/Prod23/SupplyChainManagement_Blockchain/assets/73677045/cc352fed-a402-4e5a-bf7d-cb29bd07dfa3">

<br>
<br>
Soon after Distributor1 tries to initiate a transaction with other client, known as <h3>double spending</h3> And hence, that transaction should be rejected. Here's the implementation for the same: 
<br>
<br>
<img width="935" alt="image" src="https://github.com/Prod23/SupplyChainManagement_Blockchain/assets/73677045/ed6dc9f3-be39-4d7c-a4ed-cc0d35ad424b">





## Feature -6 




### Supply Chain Blockchain: Dispute Resolution

In our Supply Chain Blockchain application, we have implemented a robust dispute resolution mechanism to handle cases where discrepancies arise between distributors and clients regarding the completion of transactions.

### How it Works:

#### 1. Transaction Confirmation via Digital Signatures:

- **Distributor's Responsibility:**
  - When a distributor dispatches a product, they generate a digital signature using their private key.
  - This digital signature is attached to the transaction data, indicating that the product has been dispatched by the distributor.

- **Client's Confirmation:**
  - When the client receives the product, they must scan the QR code associated with the transaction.
  - Scanning the QR code triggers the confirmation process.
  - If the client successfully scans the QR code, the `digitalSignature` flag associated with the transaction is set to `True`.
  - The `digitalSignature` flag serves as a confirmation that the client has received the product and verifies the authenticity of the transaction.

#### 2. Dispute Resolution:

- **Distributor Claims Transaction Completion:**
  - If the distributor claims that the transaction is complete but the `digitalSignature` flag is not set to `True`, the distributor is identified as the liar.
  - The distributor's claim is invalidated, and appropriate actions can be taken, such as deductions from the security deposit.

- **Client Denies Receiving the Product:**
  - If the client denies receiving the product but the `digitalSignature` flag is set to `True`, the client is identified as the liar.
  - The client's denial is invalidated, and necessary actions can be taken, such as deductions from the security deposit.

### Why Digital Signatures Matter:

Digital signatures ensure the integrity and authenticity of transaction data. By signing the transaction with their private key, both the distributor and the client provide cryptographic proof of their actions. This cryptographic proof serves as a reliable and secure way to confirm the completion of transactions, making the dispute resolution process transparent and trustworthy.

By leveraging digital signatures, our Supply Chain Blockchain application maintains the integrity of the supply chain, minimizes disputes, and ensures fair and reliable transactions for all participants.

--- 

Feel free to customize and expand this explanation based on the specific details of your implementation and the audience you are addressing in your README file.

