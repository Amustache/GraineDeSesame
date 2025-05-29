import bcrypt
import hashlib


def hash_password(password: str) -> (bytes, bytes):
    password_encoded = password.encode("utf-8")
    salt = bcrypt.gensalt(10)
    bcrypt_hash = bcrypt.hashpw(password_encoded, salt)
    md5_hash = hashlib.md5(password_encoded).digest()

    return md5_hash, bcrypt_hash


def check_hash(password: str, md5_hash: bytes, bcrypt_hash: bytes) -> (bool, bool):
    password_encoded = password.encode("utf-8")
    return md5_hash == hashlib.md5(password_encoded).digest(), bcrypt.checkpw(password_encoded, bcrypt_hash)


if __name__ == "__main__":
    md5_hash, bcrypt_hash = hash_password("TEST")
    print(md5_hash, bcrypt_hash)

    # Check False
    print(check_hash("test", md5_hash, bcrypt_hash))

    # Check True
    print(check_hash("TEST", md5_hash, bcrypt_hash))
