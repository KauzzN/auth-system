import jwt
import uuid
from datetime import datetime, timedelta, timezone

SECRET_KEY = "chave_super_secreta"

ALGORITHM = "HS256"

def create_access_token(user):
    
    now = datetime.now(timezone.utc)
    
    payload = {
        "sub": str(user["id"]),
        "username": user["username"],
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=15)).timestamp()),
        "jti": str(uuid.uuid4())
    }
    
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return token

def decode_access_token(token):
    
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    
    return payload