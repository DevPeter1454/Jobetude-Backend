from sqlalchemy.orm import Session
from . import models, schemas, utils
from fastapi import File, UploadFile, Form, HTTPException, status
import uuid
from typing import Annotated
from pydantic import EmailStr


          
def get_user_by_id(db:Session, user_id: uuid.uuid4):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.Users).filter(models.Users.email == email).first()

def get_company_by_email(db: Session, email: str):
    return db.query(models.Company).filter(models.Company.email == email).first()

def get_jobseeker_by_email(db: Session, email: str):
    return db.query(models.JobSeeker).filter(models.JobSeeker.email == email).first()

def get_jobseeker_by_id(db: Session, jobseeker_id: uuid.uuid4):
    return db.query(models.JobSeeker).filter(models.JobSeeker.id == jobseeker_id).first()

def get_vacancy_by_id(db: Session, vacancy_id:uuid.uuid4):
    return db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id)

def register_user(db:Session, user_credentials:schemas.UserCreate):
    user_dict = utils.schema_to_dict(user_credentials)
    user_dict['password'] = utils.hash_password(user_dict['password'])
    db_user = models.Users(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def register_employee(db:Session, file:Annotated[UploadFile,File()], employee: Annotated[schemas.EmployeeProfileCreate, Form]):
    # print('here')   
    url = utils.uploadImage(file)
    employee_dict = utils.schema_to_dict(employee)
    employee_dict['profile_img'] = url
    employee_dict['role'] = 'jobseeker'
    db_employee = models.JobSeeker(**employee_dict)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def register_company(db:Session, file:Annotated[UploadFile,File()], company: Annotated[schemas.CompanyCreate, Form]):
    url = utils.uploadImage(file)
    company_dict = utils.schema_to_dict(company)
    company_dict['profile_img'] = url
    company_dict['role'] = 'company'
    db_company = models.Company(**company_dict)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def create_vacancy(db:Session, vacancy:dict):
    db_vacancy = models.Vacancy(**vacancy)
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

def create_application(db:Session, file:UploadFile, applicant:Annotated[schemas.Application, Form] ):
    print(file.filename)
    url = utils.uploadFile(file)
    applicant_dict = utils.schema_to_dict(applicant)
    applicant_dict['jobseeker_id'] = uuid.UUID(applicant.jobseeker_id)
    applicant_dict['vacancy_id'] = uuid.UUID(applicant.vacancy_id)
    applicant_dict['resume_link'] = url
    applicant_dict['status'] = 'pending'
    db_application = models.Applications(**applicant_dict)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application
    
def check_if_applicant_already_applied(db: Session,application:schemas.Application):
    db_application = db.query(models.Applications).filter(models.Applications.jobseeker_id == application.jobseeker_id, models.Applications.vacancy_id == application.vacancy_id).first()
    return db_application