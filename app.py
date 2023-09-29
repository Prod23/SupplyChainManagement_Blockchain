from flask import Flask, jsonify,redirect, request, send_file, url_for
import json
from django.http import response
from blockchain import SupplyChainBlockchain


app = Flask(__name__)

blockchain = SupplyChainBlockchain()

@app.route("/add/users",methods=['POST'])
def add_users():
    participants = request.get_json()
    blockchain.participant(participants)

    response={
        'message' : 'the following participants have been added',
        'participants': participants
        
    }
    return jsonify(response),200


@app.route('/qrcode')
def generate_qr_code():
    if not blockchain.current_transactions: 
        return {"error": "No current transactions available"}, 400
    current_transaction = blockchain.current_transactions[-1]  # Gets the last transaction. Modify as per your use case.

    file_path = 'qr_code.png'
    blockchain.generate_qr_code(current_transaction, file_path)
    
    return send_file(file_path, mimetype='image/png', as_attachment=True, download_name='qr_code.png')


@app.route("/add/transaction",methods=['POST'])
def add_transaction():
    transaction = request.json()
    client = transaction['client']
    distributor = transaction['distributor']
    manufacturer = transaction['manufacturer']
    product=transaction['product']

    if blockchain.participants[distributor]['property'].count(property) > 0:
        blockchain.add_transaction(transaction)
        return jsonify("Transaction completed"),201
    else:
        return jsonify("Distributor does not own the mentioned properties"),201


@app.route("/chain/",methods=['GET'])
def get_chain():
    response={
        'chain':blockchain.chain,
        'length':len(blockchain.chain)

    }

    return jsonify(response),200


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

@app.route("/witnesses/",methods=['GET'])
def get_witnesses():
    response={
        'message':'the following are the witnesses',
        'witnesses':blockchain.witnesses
    }
    return jsonify(response),200


@app.route("/add/staker",methods=['POST'])
def add_staker():
    stakers = request.json()
    blockchain.add_staker(stakers)
    response={
        'message':'Kudos! the stakers have been added.',
        'stakers':stakers
    }

@app.route("/remove/staker",methods=['post'])
def remove_staker():
    staker = request.json()

    if blockchain.stakers.has_key(staker):
        blockchain.staker.pop(staker, 'the user is no more a staker')
    response={
        'message':'The following user has been removed',
        'staker':staker
    }      
    return jsonify(response), 201


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='Listening on port')
    args = parser.parse_args()
    port = args.port
    app.run(host = '0.0.0.0', port = port, debug=True)
