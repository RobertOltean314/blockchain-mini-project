import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a blockchain


class Blockchain:
    """This class is responsible for the logic of our Blockchain"""

    def __init__(self):
        """The class constructor"""
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """The function responsible for creating a new block and appending it to the blockchain"""
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """The function responsible for getting the previous block hash code"""
        return self.chain[-1]

    def proof_of_work(self, previous_proof) -> int:
        """The function responsible for the \"Proof of Work\" algorithm"""
        new_proof = 1
        check_proof = False
        while (check_proof is False):
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if (hash_operation[:4] == '0000'):
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain) -> bool:
        previous_block = chain[0]
        block_index = 1
        while (block_index < len(chain)):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']

            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


# Part 2 - Mining a Block
app = Flask(__name__)

blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof=previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations you just mine a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_blockchain_valid = blockchain.is_chain_valid(chain=blockchain.chain)

    response = {
        'message': 'The blockchain is valid' if is_blockchain_valid else 'The blockchain has some problems'
    }
    return jsonify(response), 200


app.run(host='0.0.0.0', port='5000')
