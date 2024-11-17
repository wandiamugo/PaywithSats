from ecdsa import VerifyingKey, BadSignatureError, SECP256k1

def verify_signature(public_key_hex, signature_hex, challenge):
    try:
        # Convert public key and signature
        public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
        signature = bytes.fromhex(signature_hex)

        # Verify the signature
        public_key.verify(signature, challenge.encode())
        return True
    except BadSignatureError:
        return False
