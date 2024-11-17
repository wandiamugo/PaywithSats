import os
from ecdsa import SigningKey, SECP256k1
from django.conf import settings




os.makedirs(os.path.join(settings.BASE_DIR, 'keys'), exist_ok=True)
def generate_and_save_keys(username):
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.verifying_key

    keys_dir = os.path.join(settings.BASE_DIR, 'keys')
    private_key_path = os.path.join(keys_dir, f"user_{username}_private.pem")
    public_key_path = os.path.join(keys_dir, f"user_{username}_public.pem")

    with open(private_key_path, 'wb') as private_file:
        private_file.write(private_key.to_pem())

    with open(public_key_path, 'wb') as public_file:
        public_file.write(public_key.to_pem())

    return public_key.to_pem().decode()