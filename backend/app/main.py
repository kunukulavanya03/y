from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from app.database import get_db
from app.models import User, Data
from app.schemas import UserSchema, DataSchema
from app.utils import validate_token
from datetime import datetime, timedelta
import os

load_dotenv()
cfg = BaseSettings()

crypt_context = CryptContext(schemes=['bcrypt'], default='bcrypt')

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def get_user(db, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_data(db, data_id: int) -> Data:
    return db.query(Data).filter(Data.id == data_id).first()

def validate_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return crypt_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str, db=Depends(get_db)) -> User:
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return None
    if not validate_password(password, user.password):
        return None
    return user

def get_user_by_email(email: str, db=Depends(get_db)) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(user_id: int, db=Depends(get_db)) -> User:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

def get_data_by_user_id(user_id: int, db=Depends(get_db)) -> list:
    return db.query(Data).filter(Data.user_id == user_id).all()

def generate_password() -> str:
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    return password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

app = FastAPI()

@app.get('/api/health')
def health_check() -> JSONResponse:
    return JSONResponse(content={'status': 'ok', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

@app.get('/api/users')
def get_all_users(db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> JSONResponse:
    users = db.query(User).all()
    return JSONResponse(content={'users': [user.__dict__ for user in users], 'total': len(users)})

@app.post('/api/users')
def create_user(user_schema: UserSchema, db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> JSONResponse:
    user = User(name=user_schema.name, email=user_schema.email, password=get_password_hash(user_schema.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(content={'id': user.id, 'name': user.name, 'email': user.email})

@app.get('/api/users/{user_id}')
def get_user_by_id_endpoint(user_id: int, db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> JSONResponse:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return JSONResponse(content={'id': user.id, 'name': user.name, 'email': user.email})

@app.put('/api/users/{user_id}')
def update_user_endpoint(user_id: int, user_schema: UserSchema, db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> JSONResponse:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user.name = user_schema.name
    user.email = user_schema.email
    db.commit()
    db.refresh(user)
    return JSONResponse(content={'id': user.id, 'name': user.name, 'email': user.email})

@app.delete('/api/users/{user_id}')
def delete_user_endpoint(user_id: int, db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> JSONResponse:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    db.commit()
    return JSONResponse(content={'message': 'User deleted successfully'})

@app.post('/api/login')
def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return JSONResponse(content={'access_token': access_token, 'token_type': 'bearer'})

@app.post('/api/register')
def register_endpoint(user_schema: UserSchema, db=Depends(get_db)) -> JSONResponse:
    user = User(name=user_schema.name, email=user_schema.email, password=get_password_hash(user_schema.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(content={'id': user.id, 'name': user.name, 'email': user.email})

@app.post('/api/reset-password')
def reset_password_endpoint(email: str, db=Depends(get_db)) -> JSONResponse:
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    password = generate_password()
    user.password = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return JSONResponse(content={'message': 'Password reset successfully'})

@app.get('/api/profile')
def get_profile_endpoint(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> JSONResponse:
    user_id = validate_token(token)
    user = get_user_by_id(user_id, db)
    return JSONResponse(content={'id': user.id, 'name': user.name, 'email': user.email})

@app.put('/api/profile')
def update_profile_endpoint(user_schema: UserSchema, token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> JSONResponse:
    user_id = validate_token(token)
    user = get_user_by_id(user_id, db)
    user.name = user_schema.name
    user.email = user_schema.email
    db.commit()
    db.refresh(user)
    return JSONResponse(content={'message': 'Profile updated successfully'})

@app.post('/api/data')
def create_data_endpoint(data_schema: DataSchema, token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> JSONResponse:
    user_id = validate_token(token)
    data = Data(data=data_schema.data, user_id=user_id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return JSONResponse(content={'id': data.id})

@app.get('/api/data')
def get_all_data_endpoint(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> JSONResponse:
    user_id = validate_token(token)
    data = get_data_by_user_id(user_id, db)
    return JSONResponse(content={'data': [data_schema.__dict__ for data_schema in data]})

@app.get('/api/data/{data_id}')
def get_data_by_id_endpoint(data_id: int, token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> JSONResponse:
    data = get_data(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail='Data not found')
    return JSONResponse(content={'id': data.id, 'data': data.data})

@app.put('/api/data/{data_id}')
def update_data_endpoint(data_id: int, data_schema: DataSchema, token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> JSONResponse:
    data = get_data(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail='Data not found')
    data.data = data_schema.data
    db.commit()
    db.refresh(data)
    return JSONResponse(content={'message': 'Data updated successfully'})

@app.delete('/api/data/{data_id}')
def delete_data_endpoint(data_id: int, token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> JSONResponse:
    data = get_data(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail='Data not found')
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Data deleted successfully'})