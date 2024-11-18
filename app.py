from flask import Flask, render_template, url_for, request, jsonify
from lndconnect import get_wallet_balance, generate_new_address, send_payment
# from flask import Flask, render_template, request, jsonify
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet.symbols import BTC
import os

app = Flask(__name__)


btc_user = "sawe"
btc_pass = "1234"
btc_host = "127.0.0.1"
btc_port = "38332"

def get_rpc_connection():
    return AuthServiceProxy(f"http://{btc_user}:{btc_pass}@{btc_host}:{btc_port}")


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
    
@app.route('/recover_wallet')
def recover_wallet(recover_wallet):
    return render_template('recover_wallet.html')

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
