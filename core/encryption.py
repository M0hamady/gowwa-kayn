import base64
from hashlib import pbkdf2_hmac

SECRET_SALT = b'jowwa_kayn_2026_salt_pbkdf2'
ITERATIONS = 100000

def encrypt_password(plain_password: str) -> str:
    if not plain_password:
        return ""
    if plain_password.startswith("pbkdf2_enc$"):
        return plain_password
    derived_key = pbkdf2_hmac('sha256', plain_password.encode('utf-8'), SECRET_SALT, ITERATIONS, dklen=32)
    encoded = base64.b64encode(derived_key).decode('utf-8')
    return f"pbkdf2_enc${encoded}"

def verify_password(plain_password: str, encrypted_password: str) -> bool:
    if not encrypted_password or not plain_password:
        return False
    return encrypt_password(plain_password) == encrypted_password
