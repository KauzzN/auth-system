import hashlib
from db import conn, cursor
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    
def create_refresh_token(user, raw_token):
    
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    
    query_refresh_token = """
        INSERT INTO RefreshToken (token_hash, user_id, expires_at)
        VALUES (%s, %s, %s)
    """
    
    valores = (token_hash, user["id"], expires_at)
    
    cursor.execute(query_refresh_token, valores)
    conn.commit()
    
    return raw_token