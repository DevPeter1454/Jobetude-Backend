from fastapi import APIRouter, status, Depends, HTTPException
from .. import database, models, schemas , utils, crud, oauth2
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

router = APIRouter(
    prefix="/vacancy",
    tags=["Vacancy"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_vacancy(vacancy:schemas.VacancyCreate, db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    db_company = crud.get_company_by_email(db,current_user.email)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to do this")
    vacancy_dict = utils.schema_to_dict(vacancy)
    vacancy_dict['company_id'] = db_company.id
    return crud.create_vacancy(db, vacancy_dict)
    
@router.patch("/add-requirement", status_code=status.HTTP_202_ACCEPTED)
def add_vacancy_requirements(requirements:schemas.VacancyRequirements, db: Session=Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    vacancy_id = uuid.UUID(requirements.vacancy_id)
    db_vacancy = crud.get_vacancy_by_id(db, vacancy_id)
    
    if not db_vacancy.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vacancy not found with this id {vacancy_id}")
    update_data = requirements.model_dump(exclude_unset=True)
    update_data['requirements'] = ", ".join(update_data['requirements'])
    data_to_update = {"requirements": update_data["requirements"]}
    # print(update_data['requirements'])
    db_vacancy.filter(models.Vacancy.id==vacancy_id).update(data_to_update, synchronize_session=False)
    db.commit()
    db.refresh(db_vacancy.first())
    return db_vacancy.first()


@router.get("/", status_code=status.HTTP_200_OK, )
def search_vacancy(query:Optional[str] = "", db:Session = Depends(database.get_db), limit:int = 10, skip:int = 0):

    all_vacancies = db.query(models.Vacancy).filter(models.Vacancy.open_position.ilike(f"%{query}%")).limit(limit).offset(skip).all()
    
    return all_vacancies

@router.get("/company/all", status_code=status.HTTP_200_OK)
def all_company_vacancies(db: Session = Depends(database.get_db), current_user= Depends(oauth2.get_current_user)):
    db_company = crud.get_company_by_email(db, current_user.email)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this")
    db_company_applications = db.query(models.Vacancy).filter(models.Vacancy.company_id == db_company.id).all()
    return db_company_applications


@router.get("/applications/{vacancy_id}", status_code=status.HTTP_200_OK)
def vacancy_applications(vacancy_id:str,db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user), ):
    db_company = crud.get_company_by_email(db, current_user.email)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this")
    vacancy_id = uuid.UUID(vacancy_id)
    db_vacancy_applications = db.query(models.Applications).filter(models.Applications.vacancy_id == vacancy_id).all()
    all_applicants = []
    for applicant in db_vacancy_applications:
        new_applicant = crud.get_jobseeker_by_id(db, applicant.jobseeker_id)
        all_applicants.append({
            "jobseeker": schemas.JobSeekerDetailsOut(**utils.jobseeker_to_dict(new_applicant)),
            "resume_link": applicant.resume_link,
            "status": applicant.status,
            "reply": applicant.reply,
            "application_id": applicant.id,
            "created_at": applicant.created_at,
            "updated_at": applicant.updated_at
            
        })
        
    return all_applicants
    

    
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacancy(id:uuid.UUID,db: Session = Depends(database.get_db)):
    db_vacancy = crud.get_vacancy_by_id(db, id)
    if not db_vacancy.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vacancy not found with this id {id}")
    db_vacancy.delete(synchronize_session=False)
    db.commit()
    return {"message": "Vacancy deleted successfully"}



    