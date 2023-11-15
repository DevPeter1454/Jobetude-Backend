from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, crud, database
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import EmailStr
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(user_id:UUID, db:Session = Depends(database.get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/email", status_code =status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user_by_email(email:EmailStr, db:Session = Depends(database.get_db)):
    print(email)
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.register_user(db, user)