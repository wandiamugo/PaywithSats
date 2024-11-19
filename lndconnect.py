import grpc
from lnd import lightning_pb2, lightning_pb2_grpc
# import lightning_pb2
# import lightning_pb2_grpc

LND_RPC_HOST = 'localhost:10009'
CERT_PATH = '/home/code/.lnd/tls.cert'
MACAROON_PATH = '/home/code/.lnd/data/chain/bitcoin/signet/admin.macaroon'

def connect_lnd():
    with open(CERT_PATH, 'rb') as cert_file:
        cert = cert_file.read()
    with open(MACAROON_PATH, 'rb') as macaroon_file:
        macaroon = macaroon_file.read().hex()
    creds = grpc.ssl_channel_credentials(cert)
    auth_creds = grpc.metadata_call_credentials(lambda _, callback: callback((('macaroon', macaroon),), None))
    composite_creds = grpc.composite_channel_credentials(creds, auth_creds)
    return grpc.secure_channel(LND_RPC_HOST, composite_creds)

def get_wallet_balance():
    channel = connect_lnd()
    stub = lightning_pb2_grpc.LightningStub(channel)
    response = stub.WalletBalance(lightning_pb2.WalletBalanceRequest())
    return {
        'total_balance': response.total_balance,
        'confirmed_balance': response.confirmed_balance,
        'unconfirmed_balance': response.unconfirmed_balance
    }

def generate_new_address():
    channel = connect_lnd()
    stub = lightning_pb2_grpc.LightningStub(channel)
    
    # Request a new address
    response = stub.NewAddress(lightning_pb2.NewAddressRequest())
    return response.address
def send_payment(payment_request):
    stub = connect_lnd()
    req = lightning_pb2.SendRequest(payment_request=payment_request)
    response = stub.SendPaymentSync(req)
    return {
        "payment_hash": response.payment_hash.hex(),
        "payment_preimage": response.payment_preimage.hex(),
        "payment_error": response.payment_error
    }

def get_transactions():
    channel = connect_lnd
    stub = lightning_pb2_grpc.LightningStub(channel)
    response = stub.GetTransactions(lightning_pb2.GetTransactionsRequest())
    return response.data

def send_coins(address, amount, sat_per_vbyte=None):
    try:
        channel = connect_lnd()
        stub = lightning_pb2_grpc.LightningStub(channel)
        request = lightning_pb2.SendCoinsRequest(
                addr=address,
                amount=amount,
                sat_per_vbyte=sat_per_vbyte if sat_per_vbyte else 0,
            )
        response = stub.SendCoins(request)
        return {
                "txid": response.txid,
                "amount": amount,
                "address": address,
                "status": "success",
            }
    except grpc.RpcError as e:
        return {"error": e.details()}



def create_invoice(amount, memo):
    channel = connect_lnd()
    stub = lightning_pb2_grpc.LightningStub(channel)
    invoice = lightning_pb2.Invoice(value=amount, memo=memo)
    response = stub.AddInvoice(invoice)
    return response.payment_request

def check_payment(payment_hash):
    channel = connect_lnd()
    stub = lightning_pb2_grpc.LightningStub(channel)
    req = lightning_pb2.PaymentHash(r_hash_str=payment_hash)
    response = stub.LookupInvoice(req)
    return response.settled