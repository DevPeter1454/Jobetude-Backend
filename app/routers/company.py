from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated
from .. import schemas, crud, database, utils, oauth2


router = APIRouter(
    prefix="/company",
    tags=["Company"],
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.CompanyOut)
async def create_company(file:UploadFile, company: schemas.CompanyCreate = Depends(),db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_company = crud.get_user_by_email(db, company.email)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not registered")
    return crud.register_company(db, file, company)

@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.CompanyOut)
async def get_company_details(db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_company = crud.get_company_by_email(db, current_user.email)
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return db_company
