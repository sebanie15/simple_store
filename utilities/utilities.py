

from hashlib import sha512


def encrypt(password: str):
    return sha512(bytes(password, 'utf-8')).hexdigest()


def is_phone_valid(pesel: str) -> bool:
    # TODO: write a function based on the previous one
    return True


def is_email_valid(email: str) -> bool:
    # TODO: write a function based on the previous one
    return True
