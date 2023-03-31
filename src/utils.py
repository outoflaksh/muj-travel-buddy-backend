from passlib.context import CryptContext


def hash_password(password: str):
    passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return passwd_context.hash(password)


def verify_hash(password_input, hashed_password):
    passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return passwd_context.verify(password_input, hashed_password)
