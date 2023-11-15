from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import crud, utils, schemas, models, database, oauth2
import uuid
from typing import Annotated

router = APIRouter(
    prefix= "/application",
    tags=["Job Application"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, )
def create_job_application(file:UploadFile, applicant: schemas.Application = Depends(), db: Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    print(file)
    db_employee = crud.get_jobseeker_by_email(db,current_user.email)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Employee not found')
    
    existing_application = crud.check_if_applicant_already_applied(db,applicant)
    
    if existing_application:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already applied to this job")
    
    application  = crud.create_application(db,file, applicant)
    # response = schemas.ApplicationCreateResponse(message='Success', application= application)
    return {
        "message":"Success",
        "application":application
    }
    # applicant_dict = utils.schema_to_dict(applicant)

    
    
@router.get("/my-applications", status_code=status.HTTP_200_OK)
def get_my_applications(db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_jobseeker = crud.get_jobseeker_by_email(db, current_user.email)
    if not db_jobseeker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Jobseeker with {id} not found")
    db_application = db.query(models.Applications).filter(models.Applications.jobseeker_id == db_jobseeker.id).all()
    return db_application
    
    
@router.patch("/update/reply", status_code=status.HTTP_202_ACCEPTED)
def send_application_reply(application_reply:schemas.ApplicationReply, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_company = crud.get_company_by_email(db, current_user.email)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this")
    application_reply_dict = application_reply.model_dump(exclude_unset=True)
    db_application_query = db.query(models.Applications).filter(models.Applications.id == application_reply.application_id)
    del application_reply_dict['application_id']
    db_application = db_application_query.first()
    if not db_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    db_application_query.update(application_reply_dict, synchronize_session=False)
    db.commit()
    db.refresh(db_application)
    return db_application