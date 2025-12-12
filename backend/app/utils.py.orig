from jose import jwt
from fastapi import HTTPException
from app.settings import Settings

def validate_token(token: str):
    try:
        payload = jwt.decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        user_id: str = payload.get('sub')
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')