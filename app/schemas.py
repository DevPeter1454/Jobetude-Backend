from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional, Union
from dataclasses import dataclass
from fastapi import Form
from uuid import UUID
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str = None
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str = None
    role: Optional[str] = None

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
    
class ForgotPassword(BaseModel):
    identifier: str 

class ResetPassword(BaseModel):
    password: str
    confirm_password: str
    token: str

@dataclass
class EmployeeProfileCreate:
    role: str = "employee"
    fullname: str = Form(...)
    email: EmailStr = Form(...)
    date_of_birth: datetime = Form(...)
    address: str = Form(...)
    occupation: str = Form(...)
        
class EmployeeOut(BaseModel):
    id: UUID
    fullname: str
    email: EmailStr
    date_of_birth: datetime
    address: str
    occupation: str
    profile_img: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VacancyCreate(BaseModel):
   open_position: str
   salary: int
   location: str
   type: str
   active: bool = True
   company_id: str
   category : str
   
class VacancyRequirements(BaseModel):
    vacancy_id: str
    requirements: List[str]   

class Vacancy(BaseModel):
    id: int
    open_position: str
    salary: str
    location: str
    type: str
    active: bool
    requirements: List[str]
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        

# class EmployeeApplication(BaseModel):
@dataclass   
class CompanyCreate:
    company_name: str = Form(...)
    email: EmailStr = Form(...)
    established_date: datetime = Form(...)
    country: str = Form(...)
    company_address:str = Form(...)


class CompanyOut(BaseModel):
    # id: int
    company_name: str
    email: EmailStr
    established_date: datetime
    country: str
    company_address: str
    profile_img: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
    
class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    id: Optional[UUID] = None
    
class AccessTokenData(BaseModel):
    access_token: str
    token_type: str
    message: Optional[str] = None
    
class Login(BaseModel):
    email: EmailStr
    password: str
    
class EmployeeProfileUpdate(BaseModel):
    fullname: str | None = None
    email: EmailStr | None = None
    date_of_birth: datetime | None = None
    address: str | None = None
    occupation: str | None = None
    profile_img: str | None = None
   
@dataclass 
class Application:
    jobseeker_id:str = Form(...)
    vacancy_id:str = Form(...)
    bookmarked: bool| None = False

class ApplicationOut(BaseModel):
    jobseeker_id: UUID
    vacancy_id: UUID
    created_at: datetime
    updated_at: datetime
    resume_link: str
    status: str
    reply:str | None = None
    bookmarked: bool | None = False
    
class ApplicationCreateResponse(BaseModel):
    message: str
    application: ApplicationOut   
    
class JobSeekerDetailsOut(BaseModel):
    fullname:str
    profile_img: str
    email:EmailStr
    occupation:str
    
    class config:
        from_attributes = True
 
class ApplicationReply(BaseModel):
    reply: str
    application_id: str
    status: str 
    interview_date: datetime | None = None