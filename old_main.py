from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates 
from sqlmodel import SQLModel, Field
from sqlmodel import Session,create_engine,select
from typing import Annotated
from fastapi import Depends
from fastapi import Form


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

class User(SQLModel,table = True):
    user_id: int | None = Field(default=None, primary_key=True)
    user_name: str
    password: str

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


@app.post("/sign_up")
def sign_up(
    user_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: SessionDep
):
    user = User(user_name=user_name, password=password)

    session.add(user)
    session.commit()
    session.refresh(user)

    RedirectResponse(url=f"/create_portfolio/{user_name}", status_code=303)

@app.get("/sign_up",response_class=HTMLResponse)
def sign_up(request:Request,session:SessionDep):
    return templates.TemplateResponse(
        request=request,
        name="sign_up.html"
    )

@app.post("/create_portfolio/{user_name}")
def add_person(name: Annotated[str,Form()],
             email:  Annotated[str,Form()],
            experience: Annotated[str,Form()],
            education: Annotated[str,Form()],
            projects: Annotated[str,Form()],
            session : SessionDep
):      
    person = Person(name =name,
                    email=email,
                    experience= experience,
                    education = education,
                    projects = projects)
    session.add(person)
    session.commit()
    session.refresh(person)
    return 

@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: SessionDep):
    people = session.exec(select(Person)).all()
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"people": people}
    )

@app.get("/create_portfolio/{user_name}", response_class=HTMLResponse)
def create_portfolio_page(user_name: str, request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_portfolio.html",
        context={"user_name": user_name}
    )



