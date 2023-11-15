# from jose import JWTError, jwt
from passlib.context import CryptContext
import cloudinary
import cloudinary.uploader
import requests
from fastapi import File, UploadFile
from tempfile import NamedTemporaryFile
import os
from . import config

cloudinary.config( 
  cloud_name = f"{config.settings.cloudinary_cloud_name}", 
  api_key = f"{config.settings.cloudinary_api_key}", 
  api_secret = f"{config.settings.cloudinary_api_secret}" 
)




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def uploadImage(file:UploadFile):
    response = cloudinary.uploader.upload(file.file)
    # print(response)
    return response['url']

def uploadFile(file:UploadFile):
    with NamedTemporaryFile(delete=False) as temp_pdf_file:
        temp_pdf_path = temp_pdf_file.name
        temp_pdf_file.write(file.file.read())
    
    response = cloudinary.uploader.upload(temp_pdf_path)
    
    os.remove(temp_pdf_path)
    
    return response['url']


def schema_to_dict(schema):
    return {k:v for k,v in schema.__dict__.items() if not k.startswith("_")}

def jobseeker_to_dict(jobseeker):
    return {
        column.key: getattr(jobseeker, column.key)
        for column in jobseeker.__table__.columns
    }
    