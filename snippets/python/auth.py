import jwt
from datetime import timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def authenticate_user(email: str, password: str) -> dict:
    # verify user credentials, query DB
    # return {'user_id': int, 'token': str}
    pass

def verify_token(token: str) -> int:
    # decode and validate JWT
    # return user_id
    pass
