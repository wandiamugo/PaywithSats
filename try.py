from flask import Flask, jsonify, request
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from mnemonic import Mnemonic
import os
import binascii
import hashlib
from hdwallet import HDWallet
from hdwallet.symbols import BTC
from typing import Optional

app = Flask(__name__)

# Bitcoin RPC setup
btc_user = "username"
btc_pass = "password"
btc_host = "127.0.0.1"
btc_port = "18443"

def get_rpc_connection():
    return AuthServiceProxy(f"http://{btc_user}:{btc_pass}@{btc_host}:{btc_port}")

def generate_seed_and_addresses():
    # Generate mnemonic (recovery phrase)
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=256)  # 24 words
    seed = mnemo.to_seed(mnemonic)

    # Initialize HD wallet
    hdwallet: HDWallet = HDWallet(symbol=BTC)
    hdwallet.from_seed(seed=seed)

    # Derive the first address (m/44'/0'/0'/0/0)
    hdwallet.from_path("m/44'/0'/0'/0/0")

    wallet_info = {
        'mnemonic': mnemonic,
        'seed': seed.hex(),
        'address': hdwallet.p2pkh_address(),
        'private_key': hdwallet.private_key(),
        'public_key': hdwallet.public_key()
    }
    
    return wallet_info
@app.route('/hello')
def hello():
    return "hello_wordl"
    

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    try:
        rpc_connection = get_rpc_connection()
        
        # Generate wallet info with mnemonic
        wallet_info = generate_seed_and_addresses()
        
        # Create wallet name using first 8 chars of address
        wallet_name = f"wallet_{wallet_info['address'][:8]}"
        
        # Create new wallet in Bitcoin Core
        result = rpc_connection.createwallet(wallet_name)
        
        # Import the private key
        rpc_connection.importprivkey(wallet_info['private_key'], "primary", False)
        
        return jsonify({
            'status': 'success',
            'message': f'Wallet {wallet_name} created successfully',
            'wallet_name': wallet_name,
            'mnemonic': wallet_info['mnemonic'],
            'address': wallet_info['address'],
            'warning': 'IMPORTANT: Please save your mnemonic phrase securely. It cannot be recovered if lost!'
        })

    except JSONRPCException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recover_wallet', methods=['POST'])
def recover_wallet():
    try:
        if not request.json or 'mnemonic' not in request.json:
            return jsonify({'error': 'Mnemonic phrase is required'}), 400

        mnemonic = request.json['mnemonic']
        
        # Validate mnemonic
        mnemo = Mnemonic("english")
        if not mnemo.check(mnemonic):
            return jsonify({'error': 'Invalid mnemonic phrase'}), 400

        # Generate seed from mnemonic
        seed = mnemo.to_seed(mnemonic)

        # Initialize HD wallet
        hdwallet: HDWallet = HDWallet(symbol=BTC)
        hdwallet.from_seed(seed=seed)

        # Derive the first address
        hdwallet.from_path("m/44'/0'/0'/0/0")

        # Create wallet in Bitcoin Core
        rpc_connection = get_rpc_connection()
        wallet_name = f"recovered_{hdwallet.p2pkh_address()[:8]}"
        
        result = rpc_connection.createwallet(wallet_name)
        
        # Import the private key
        rpc_connection.importprivkey(hdwallet.private_key(), "recovered", False)

        return jsonify({
            'status': 'success',
            'message': 'Wallet recovered successfully',
            'wallet_name': wallet_name,
            'address': hdwallet.p2pkh_address()
        })

    except JSONRPCException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Generate new address for receiving
@app.route('/generate_address', methods=['GET'])
def generate_address():
    try:
        rpc_connection = get_rpc_connection()
        
        # Generate new address
        address = rpc_connection.getnewaddress()
        
        return jsonify({
            'status': 'success',
            'address': address
        })
    except JSONRPCException as e:
        return jsonify({'error': str(e)}), 500

# Send Bitcoin
@app.route('/send_payment', methods=['POST'])
def send_payment():
    try:
        if not request.json or 'address' not in request.json or 'amount' not in request.json:
            return jsonify({'error': 'Missing address or amount'}), 400

        address = request.json['address']
        amount = float(request.json['amount'])
        
        rpc_connection = get_rpc_connection()
        
        # Validate address
        valid = rpc_connection.validateaddress(address)
        if not valid['isvalid']:
            return jsonify({'error': 'Invalid Bitcoin address'}), 400

        # Check balance
        balance = rpc_connection.getbalance()
        if balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400

        # Send transaction
        txid = rpc_connection.sendtoaddress(address, amount)
        
        return jsonify({
            'status': 'success',
            'txid': txid,
            'amount': amount,
            'recipient': address
        })
    except JSONRPCException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
