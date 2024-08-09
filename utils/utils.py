from datetime import datetime, timedelta, timezone
import bcrypt
import jwt


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "batatafricacombanana", algorithm="HS256")
    return encoded_jwt


# criar um hash da senha e retornar o hash
def encrypt_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    # return {"hash_password": hashed_password, "salt": salt}
    return hashed_password.decode()


# True = senha certa
# False = senha incorreta
def check_password(hashed_password: str, password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def validate_token(headers):
    authorization_header = headers.get("authorization")
    token = authorization_header[7:] if authorization_header and authorization_header.startswith("Bearer ") else None
    return token


