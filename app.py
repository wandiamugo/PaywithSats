from flask import Flask, render_template, url_for, request, jsonify
from lndconnect import get_wallet_balance, generate_new_address, send_payment, send_coins
# from flask import Flask, render_template, request, jsonify
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet.symbols import BTC
import os
import requests
import json

app = Flask(__name__)


btc_user = "sawe"
btc_pass = "1234"
btc_host = "127.0.0.1"
btc_port = "38332"

def get_rpc_connection():
    return AuthServiceProxy(f"http://{btc_user}:{btc_pass}@{btc_host}:{btc_port}")

def generate_seed_and_addresses():
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=256)

    # Check if mnemonic is valid
    if not mnemo.check(mnemonic):
        raise ValueError("Generated mnemonic is invalid.")

    # Generate the seed from the mnemonic
    seed = mnemo.to_seed(mnemonic)

    # Ensure the seed is a byte object before converting to hex
    if isinstance(seed, bytes):
        # Convert the seed bytes to a hex string (should not raise "Non-hexadecimal digit found")
        seed_hex = seed.hex()
    else:
        raise ValueError("Seed is not in valid byte format.")

    # Initialize HDWallet with the generated seed
    hdwallet = HDWallet(symbol=BTC)
    hdwallet.from_seed(seed=seed)
    hdwallet.from_path("m/44'/0'/0'/0/0")  # Derive the first address

    # Return the wallet data, including mnemonic, seed, address, private key, and public key
    return {
        'mnemonic': mnemonic,
        'seed': seed_hex,
        'address': hdwallet.p2pkh_address(),
        'private_key': hdwallet.private_key(),
        'public_key': hdwallet.public_key()
    }

@app.route('/')
def index():
    return render_template('index.html', title='Payment System')

@app.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    wallet_name = request.form.get('wallet_name')
    if not wallet_name:
        return render_template('create_wallet.html'
                            #    , jsonify({"error": "Wallet name is required"})
                               ), 400

    try:
        # Connect to Bitcoin Core
        rpc_connection = AuthServiceProxy("http://sawe:1234@127.0.0.1:38332")
        
        # Create wallet
        result = rpc_connection.createwallet(wallet_name)
        return render_template('create_wallet_response.html',
            message="Wallet created successfully",
            wallet_name= wallet_name,
            details= result
        )
    except JSONRPCException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recover_wallet', methods=['GET', 'POST'])
def recover_wallet():
    if request.method == 'POST':
        try:
            mnemonic = request.form['seed']
            mnemo = Mnemonic("english")
            if not mnemo.check(mnemonic):
                return render_template('recover_wallet.html', error="Invalid mnemonic phrase")
            seed = mnemo.to_seed(mnemonic)
            hdwallet = HDWallet(symbol=BTC)
            hdwallet.from_seed(seed=seed)
            hdwallet.from_path("m/44'/0'/0'/0/0")
            rpc_connection = get_rpc_connection()
            wallet_name = f"recovered_{hdwallet.p2pkh_address()[:8]}"
            rpc_connection.createwallet(wallet_name)
            rpc_connection.importprivkey(hdwallet.private_key(), "recovered", False)
            return render_template('success.html', wallet_name=wallet_name, address=hdwallet.p2pkh_address())
        except JSONRPCException as e:
            return jsonify({'error': str(e)}), 500
    return render_template('recover_wallet.html')


@app.route('/send_payment', methods=['GET', 'POST'])
def send_payment():
    if request.method == 'POST':
        try:
            address = request.form['address']
            amount = float(request.form['amount'])
            rpc_connection = AuthServiceProxy("http://sawe:1234@127.0.0.1:38332/wallet/signetwallet1")
            valid = rpc_connection.validateaddress(address)
            if not valid['isvalid']:
                return render_template('send.html', error="Invalid Bitcoin address")
            balance = rpc_connection.getbalance()
            if balance < amount:
                return render_template('send.html', error="Insufficient funds")
            txid = rpc_connection.sendtoaddress(address, amount)
            balance =rpc_connection.getbalance()
            return render_template('success.html', txid=txid, amount=amount, recipient=address , balance=balance)
        except JSONRPCException as e:
            return jsonify({'error': str(e)}), 500
    return render_template('send.html')

# @app.route('/get_balance', methods=['GET'])
# def send_payment():
#     if request.method == 'GET':
#         try:
#             rpc_connection = AuthServiceProxy("http://sawe:1234@127.0.0.1:38332/wallet/signetwallet1")


@app.route('/send_to_address', methods=['GET', 'POST'])
def send_to_address(rpc_user, rpc_password, address, amount, rpc_port=38332, rpc_host='127.0.0.1'):
    url = f"http://{rpc_host}:{rpc_port}/"
    headers = {'content-type': 'application/json'}

    # Prepare the RPC payload
    payload = json.dumps({
        "method": "sendtoaddress",
        "params": [address, amount],
        "id": 1,
        "jsonrpc": "2.0"
    })
    try:
        # Make the RPC call
        response = requests.post(url, headers=headers, data=payload, auth=(rpc_user, rpc_password))
        response_data = response.json()

        # Check for errors in the RPC response
        if response.status_code == 200 and 'error' not in response_data:
            return {
                "txid": response_data['result'],
                "address": address,
                "amount": amount,
                "status": "success"
            }
        else:
            return {
                "error": response_data.get('error', {}).get('message', 'Unknown error'),
                "status": "failure"
            }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status": "failure"}
    
@app.route('/check_balance', methods=['GET'])
def check_balance():
    rpc_connection = AuthServiceProxy("http://sawe:1234@127.0.0.1:38332/wallet/signetwallet1")
    balance =rpc_connection.getbalance()
    return render_template('balance.html', balance=balance)



# @app.route('/recover_wallet')
# def recover_wallet(recover_wallet):
#     return render_template('recover_wallet.html')

@app.route('/balance', methods=['GET'])
def balance_route():
    try:
        balance = get_wallet_balance()
        return jsonify(balance), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/new_address')   
def generate_address_view():
    try:
        # address_type = request.GET.get('address_type', 'p2wkh')
        address = generate_new_address()
        return jsonify({'address' : address }), 200
    except Exception as e:
        return jsonify({'error': str(e)}, status=500)
    
@app.route('/send_coins', methods=['POST'])
def send_coins_route():
    """
    Flask route to send coins using the LND API.
    """
    try:
        data = request.get_json()
        address = data.get('address')
        amount = data.get('amount')
        sat_per_vbyte = data.get('sat_per_vbyte', None)

        if not address or not amount:
            return jsonify({"error": "Address and amount are required"}), 400

        result = send_coins(address, amount, sat_per_vbyte)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send', methods=['POST'])
def send_route():
    try:
        data = request.get_json()
        payment_request = data.get("payment_request")
        if not payment_request:
            return jsonify({"error": "Payment request is required"}), 400

        result = send_payment(payment_request)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
