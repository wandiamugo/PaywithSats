import os
import binascii
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from ecdsa import VerifyingKey, BadSignatureError, SECP256k1, SigningKey
from django.http import JsonResponse
from .models import User, Service
from .createkeys import generate_and_save_keys
from .lndconnect import generate_new_address, get_wallet_balance, get_transactions

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'})

        # Generate public/private keys and save the public key
        public_key = generate_and_save_keys(username)

        # Save the user in the database
        User.objects.create(username=username, public_key=public_key)

        return JsonResponse({'message': 'User registered successfully', 'public_key': public_key})
    return render(request, 'register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print(f"Login Session Key: {request.session.session_key}")
        private_key_pem = open('keys/user_dee_private.pem', 'rb').read()
        private_key = SigningKey.from_pem(private_key_pem)
        username = request.POST.get('username')
        challenge = os.urandom(16).hex()  # Generate a random challenge
        # request.session['challenge'] = challenge
        signature = private_key.sign(challenge.encode())

        # Hex encode the signature for transmission
        signature_hex = binascii.hexlify(signature).decode()

        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'error': 'User not found'})

        return JsonResponse({'challenge': challenge, 'public_key': user.public_key, 'signature': signature_hex})
    return render(request, 'login.html')
@csrf_exempt
def verify(request):
    if request.method == 'POST':
        print(f"Verify Session Key: {request.session.session_key}")
        data = json.loads(request.body)
        challenge = request.session.get('challenge')
        print(challenge)
        
        username = data['username']
        signature_hex = data['signature']

        

        try:
            # Retrieve the user
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        # Retrieve the public key stored for the user
        public_key_pem = user.public_key
        
        # Decode the public key from PEM format
        public_key = VerifyingKey.from_pem(public_key_pem.encode())
        
        # Retrieve the challenge stored in the session
        challenge = request.session.get('challenge')
        print(challenge)

        if not challenge:
            return JsonResponse({'error': 'Challenge not found in session'}, status=400)
        
        # Convert the signature from hex to binary
        signature = binascii.unhexlify(signature_hex)

        try:
            # Verify the signature against the challenge
            # print(signature)
            # print(signature_hex)
            print(challenge)
            # print(challenge.encode())
            public_key.verify(signature, challenge.encode())
            return JsonResponse({'message': 'Login successful'})
        except BadSignatureError:
            return JsonResponse({'error': 'Invalid signature'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def wallet_balance_view(request):
    try:
        balance = get_wallet_balance()
        print(balance)
        return JsonResponse({'balance': balance})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def generate_address_view(request):
    try:
        # address_type = request.GET.get('address_type', 'p2wkh')
        address = generate_new_address()
        return JsonResponse({'address': address})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def get_transactions_view(request):
    try:
        transactions = get_transactions()
        return JsonResponse({'transactions': transactions})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



# def pay_for_service(request, content_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')
#     content = Service.objects.get(id=content_id)
#     payment_request = create_invoice(content.price, f"Payment for {content.title}")
#     return render(request, 'payment.html', {'payment_request': payment_request})

# def payment_status(request, payment_hash):
#     if check_payment(payment_hash):
#         return JsonResponse({'status': 'Payment complete'})
#     return JsonResponse({'status': 'Payment pending'})
