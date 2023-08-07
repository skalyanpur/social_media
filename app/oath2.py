from datetime import datetime, timedelta

from jose import jwt

# Secret key
SECRET_KEY = "d7f28b0e502053c30f0bbc6f4e8148fdbddc5b50773fa168b744b32ac542d432"
# algorithm
ALGORITHM = "HS256"
# expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt
