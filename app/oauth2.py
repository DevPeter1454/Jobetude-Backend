from fastapi import Depends, HTTPException, status
from . import schemas, database, models, crud
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Annotated
import uuid
import json
from sqlalchemy.orm import Session

SECRET_KEY = "0c18fe7b30c167f3404e061423212bca0a83998793c58dbccaa3b247e3c257fb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id = uuid.UUID(payload.get("id"))
        
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(email=email,  id=id)
        return token_data
    except JWTError:
        raise credentials_exception

def get_current_user(token:Annotated[str,Depends(oauth2_scheme)], db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user = verify_token(token, credentials_exception)
    db_user = crud.get_user_by_email(db, user.email)
    if db_user is None:
        raise credentials_exception
    return db_user
    
        
