#importing necessary libraries
from flask import Flask, jsonify,redirect, request, send_file, url_for
import json
from django.http import response
from blockchain import SupplyChainBlockchain
import uuid

#intitializing flask
app = Flask(__name__)
blockchain = SupplyChainBlockchain()


#api call for adding a users.
@app.route("/add/users",methods=['POST'])
def add_users():
    participants = request.get_json()
    for key, value in participants.items():
        if value["type"] == "distributor":
            value["private_key"] = str(uuid.uuid4()).replace("-", "")

    blockchain.participant(participants)
    response={
        'message' : 'the following participants have been added',
        'participants': participants
    }
    return jsonify(response),200

#API call for listing the users added.
@app.route("/users")
def show_users():
    participants = blockchain.participants
    response={
        'participants':participants
    }

    return jsonify(response),200

#API call for generating the qrcode of product status of the latest transaction.
@app.route('/qrcode',methods=['GET'])
def generate_qr_code():
    if not blockchain.current_transactions: 
        return {"error": "No current transactions available"}, 400
    current_transaction = blockchain.current_transactions[-1]  # Gets the last transaction.

    file_path = 'qr_code.png'
    blockchain.generate_qr_code(current_transaction, file_path)
    
    return send_file(file_path, mimetype='image/png', as_attachment=True, download_name='qr_code.png')


#API call for adding a transaction
@app.route("/add/transaction",methods=['POST'])
def add_transaction():
    transaction_data = request.json
    client = transaction_data.get('client')
    product=transaction_data.get('product')
    distributor = transaction_data.get('distributor')
    distributor_data = blockchain.participants[distributor]
    
    if distributor not in blockchain.participants:
        return jsonify({"error": "Distributor does not exist"}), 400  # Use 400 for client errors
    
    if distributor in blockchain.deliveries_in_progress:
        return jsonify("Distributor is currently engaged in another transaction"), 400
    
    if 'property' in distributor_data and product in distributor_data['property']:
        blockchain.add_transaction(manufacturer=transaction_data.get('manufacturer', ''), distributor=distributor, client=client, product=product, amount=transaction_data.get('amount', 0))
        blockchain.deliveries_in_progress[distributor] = client  # Mark the distributor as engaged in a delivery
        return jsonify("Transaction added"),200
    
    else:
        return jsonify("Distributor does not own the mentioned properties"),201


#API call for generating the blockchain and listing the blocks with transactions.
@app.route("/chain/",methods=['GET'])
def get_chain():
    response={
        'chain':blockchain.chain,
        'length':len(blockchain.chain)

    }

    return jsonify(response),200


#API call for the voting process.
@app.route("/voting",methods=['GET'])
def voting():
    if port == 5001:
        blockchain.dpos_vote()
        blockchain.dpos_result()

        response={
            'message':"Voting has been successfull and as follows: ",
            'nodes:':blockchain.delegates
        }

        return jsonify(response),200
    else:
        response={
            'message':'you are not authorised to conduct the voting process'
        }

        return jsonify(response),200

#API call for finding out the witnesses.
@app.route("/witnesses/",methods=['GET'])
def get_witnesses():
    response={
        'message':'the following are the witnesses',
        'witnesses':blockchain.witnesses
    }
    return jsonify(response),200

#route for adding a staker in the blockchain.
@app.route("/add/staker",methods=['POST'])
def add_staker():
    stakers = request.json
    blockchain.add_staker(stakers)
    response={
        'message':'Kudos! the stakers have been added.',
        'stakers':stakers
    }

    return jsonify(response), 201


#route for removing a staker from the blockchain.
@app.route("/remove/staker",methods=['post'])
def remove_staker():
    staker = request.json

    if blockchain.stakers.has_key(staker):
        blockchain.staker.pop(staker, 'the user is no more a staker')
    response={
        'message':'The following user has been removed',
        'staker':staker
    }      
    return jsonify(response), 201


#route for resolving any disputes.
@app.route("/dispute",methods=['GET'])
def dispute():

    if blockchain.digitalSignature:
        response={
            'message':'No disputes'
        }
    else:
        response={
            'message':'There is a dispute'
        }
    return jsonify(response),200    

#API call for mining a block.
@app.route("/mine",methods=['GET'])
def mine_block():
    if len(blockchain.unverified_transactions)>=2:
        block = blockchain.create_block()
        blockchain.digitalSignature = True
        response={
            'message':'New block Mined!',
            'index':block['index'],
            'timestamp':block['timestamp'],
            'transactions': block['transactions'],
            'merkle_root': block['merkle_root'],
            'previous_hash': block['previous_hash']

        }
        print(len(blockchain.unverified_transactions))
        return jsonify(response), 200
    
    else:
        response = {
                'message' : 'Not enough transactions to mine a new block and add to chain!'
            }
        print(len(blockchain.unverified_transactions))
        return jsonify(response), 400
    

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='Listening on port')
    args = parser.parse_args()
    port = args.port
    app.run(host = '0.0.0.0', port = port, debug=True)
