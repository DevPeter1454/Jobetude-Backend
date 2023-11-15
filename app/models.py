from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('NOW()'))
    updated_at = Column(TIMESTAMP, server_default=text('NOW()'), onupdate=text('NOW()'))
    jobseeker = relationship("JobSeeker", back_populates="user", primaryjoin="Users.email==JobSeeker.email")
    company = relationship("Company", back_populates="user", primaryjoin="Company.email==Users.email")

class JobSeeker(Base):
    __tablename__ = "jobseeker"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4, unique=True, index=True, )
    email = Column(String, ForeignKey("users.email", onupdate="CASCADE", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    fullname = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    address = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    profile_img = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('NOW()'))
    updated_at = Column(TIMESTAMP, server_default=text('NOW()'), onupdate=text('NOW()'))
    role = Column(String, nullable=True)
    applications = relationship("Applications", back_populates="jobseeker", primaryjoin="JobSeeker.id==Applications.jobseeker_id")
    user = relationship("Users", back_populates="jobseeker", primaryjoin="Users.email==JobSeeker.email")

class Company(Base):
    __tablename__ = "company"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    email = Column(String, ForeignKey("users.email",onupdate="CASCADE", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    company_name = Column(String, nullable=True)
    company_address = Column(String, nullable=True)
    profile_img = Column(String, nullable=True)
    established_date = Column(DateTime, nullable=True)
    country = Column(String, nullable=True)
    role = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('NOW()'))
    updated_at = Column(TIMESTAMP, server_default=text('NOW()'), onupdate=text('NOW()'))
    vacancies = relationship("Vacancy", back_populates="company")
    user = relationship("Users", back_populates="company", primaryjoin="Users.email==Company.email")

    
class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    open_position = Column(String, nullable= False)
    salary = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    type = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, )
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)
    requirements = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('NOW()'))
    updated_at = Column(TIMESTAMP, server_default=text('NOW()'), onupdate=text('NOW()'))
    company = relationship("Company", back_populates="vacancies", primaryjoin="Company.id==Vacancy.company_id")
    
class Applications(Base):
    __tablename__ = "applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    jobseeker_id = Column(UUID(as_uuid=True), ForeignKey('jobseeker.id'), nullable=False)
    vacancy_id = Column(UUID(as_uuid=True), ForeignKey('vacancy.id'), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('NOW()'))
    updated_at = Column(TIMESTAMP, server_default=text('NOW()'), onupdate=text('NOW()'))
    reply = Column(String, nullable=True)
    bookmarked = Column(Boolean, nullable=True, default=False)
    resume_link = Column(String, nullable=False)
    interview_date = Column(DateTime, nullable=True)
    jobseeker = relationship("JobSeeker", back_populates="applications", primaryjoin="JobSeeker.id==Applications.jobseeker_id")
    

    

