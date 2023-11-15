from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import database, models
from .routers import employee, company, auth, users, vacancy, applications



# models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(employee.router)
app.include_router(company.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(vacancy.router)
app.include_router(applications.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}