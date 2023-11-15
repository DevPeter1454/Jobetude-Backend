from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from .. import crud , database, schemas, utils, oauth2, models
from sqlalchemy.orm import Session
from typing import Annotated
import uuid
from pydantic import EmailStr
router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
)

@router.post("/create", status_code=status.HTTP_201_CREATED,response_model=schemas.EmployeeOut )
def create_employee(file:UploadFile, employee: schemas.EmployeeProfileCreate = Depends(), db: Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user) ):
    db_employee = crud.get_jobseeker_by_email(db, employee.email)
    if  db_employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.register_employee(db,file, employee)

@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.EmployeeOut)
def get_employee_details(db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_employee = crud.get_jobseeker_by_email(db, current_user.email)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return db_employee

@router.patch("/update", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.EmployeeOut)
def update_profile(payload:schemas.EmployeeProfileUpdate, db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_employee_query = db.query(models.JobSeeker).filter(models.JobSeeker.email == current_user.email)
    db_employee = db_employee_query.first()
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    payload_dict = payload.model_dump(exclude_unset=True)
    if "email" in payload_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email cannot be updated")
    db_employee_query.update(payload_dict, synchronize_session=False)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.delete("/delete", status_code=status.HTTP_202_ACCEPTED)
def delete_account(db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_employee = crud.get_jobseeker_by_email(db, current_user.email)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    db_employee.delete(synchronize_session=False)
    db.commit()
    return {"message": "Account deleted successfully"}
