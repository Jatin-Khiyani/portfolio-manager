from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, Session, select



app = FastAPI()

templates = Jinja2Templates(directory="HTML")


# Database for storing login information
class Sign_Up(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    user_name: str
    password: str

# Database for storing user data for portfolio
class Person(SQLModel,table = True):
    person_id: int | None = Field(default=None, primary_key=True)
    name: str
    email:str
    experience: str
    education: str
    projects: str



# setting up sql database
sqlite_file_name = "portfolio_manager_db.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def create_db():
    SQLModel.metadata.create_all(engine)


# HOW DOES THIS CREATE SESSION NEED TO UNDERSTAND
def get_session():
    with Session(engine) as session:
        yield session


# NEED TO GET A BETTER UNDERSTANDIG OF SESSIONS AND DEPENDS
SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db()


# Home Page
@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


# Sign up Page
@app.get("/sign-up", response_class=HTMLResponse)
def sign_up_page(request: Request):
    return templates.TemplateResponse(request=request, name="sign-up.html")

# Sign In page
@app.get("/sign-in",response_class=HTMLResponse)
def sign_in_page(request:Request):
    return templates.TemplateResponse(request=request,name="sign-in.html")

# Saving sign_up deatils to the database
@app.post("/sign-up")
def store_login_information(user_name: Annotated[str,Form()], password: Annotated[str,Form()], session: SessionDep):
    sign_up = Sign_Up(user_name=user_name, password=password)
    session.add(sign_up)
    session.commit()
    session.refresh(sign_up)

    return RedirectResponse(url=f"/create_portfolio/{user_name}", status_code=303)

# Sign in page and login (checking username and password)
@app.post("/sign-in")
def check_login_information(user_name: Annotated[str,Form()], password: Annotated[str,Form()], session: SessionDep,request:Request):

    statement = select(Sign_Up).where(Sign_Up.user_name==user_name,Sign_Up.password==password)
    sign_up = session.exec(statement).first()

    if sign_up:
        return RedirectResponse(url=f"/create_portfolio/{user_name}", status_code=303)
    else: 
         return templates.TemplateResponse(
            name = "sign-in.html",
            request = request, 
            context =  {"error" : "Could not find username and password, please try again"}
        )
    
@app.get(f"/create_portfolio/{Sign_Up.user_name}")
def create_portfolio_page(request:Request):
    return templates.TemplateResponse(request = request,name="create_portfolio.html")

@app.post(f"/create_portfolio/{Sign_Up.user_name}")
def store_person_data(name: Annotated[str, Form()],email: Annotated[str, Form()],experience: Annotated[str, Form()],education: Annotated[str, Form()],projects: Annotated[str, Form()],session: SessionDep,request:Request):
    #### Make this Function in the next sprint. 

