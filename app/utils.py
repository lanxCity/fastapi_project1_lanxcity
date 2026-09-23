# for hashing password
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash(password: str) -> str:
    return password_hash.hash(password)

def verify(plain_test, hashed_password):
    return password_hash.verify(plain_test, hashed_password)