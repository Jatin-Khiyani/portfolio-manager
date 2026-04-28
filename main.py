from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 
from sqlmodel import SQLModel, Field
from sqlmodel import Session,create_engine,select
from typing import Annotated
from fastapi import Depends


app = FastAPI()

templates = Jinja2Templates(directory="templates") 
welcome_msg = "Profile for user"

# SQL Model 
class Person(SQLModel,table = True):
    person_id: int | None = Field(default=None, primary_key=True)
    name: str
    email:str
    experience: str
    education: str
    projects: str

# Setting Up SQLModel Database



sqlite_file_name = "database.db"
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url,connect_args= {"check_same_thread" : False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/people")
def add_person(person: Person,session : SessionDep):
    session.add(person)
    session.commit()
    session.refresh(person)
    return {
        "message": "Person added successfully",
        "data": person
    }

# HOME → list names
@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: SessionDep):
    people = session.exec(select(Person)).all()
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "people": people}
    )

# PROFILE → by name
@app.get("/profile/{name}", response_class=HTMLResponse)
def profile(name: str, request: Request, session: SessionDep):
    person = session.exec(select(Person).where(Person.name == name)).first()
    return templates.TemplateResponse(
        "index_updated.html",
        {"request": request, "person": person}
    )

# @app.get("/people/{person_id}/profile", response_class=HTMLResponse)
# def get_person_profile(person_id: int):
#     if person_id in people_db:
#         person = people_db[person_id]
#         return templates.TemplateResponse("profile.html", {"request": {}, "person": person})
#     return {"error": "Person not found"}

