from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from .. import schemas, crud, database, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
import uuid
import json

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.AccessTokenData)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user_credentials.username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not utils.verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
   
    access_token = oauth2.create_access_token(data={"sub": db_user.email, "id": str(db_user.id)})
    
    # print(access_token)
    token_user_data = schemas.AccessTokenData(access_token=access_token, token_type="bearer", message="Login Successful")
    return token_user_data