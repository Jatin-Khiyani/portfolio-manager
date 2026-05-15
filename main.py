from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, Session



app = FastAPI()

templates = Jinja2Templates(directory="HTML")


# Database for storing login information
class Sign_Up(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    user_name: str
    password: str



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
def sign_in(request:Request):
    return templates.TemplateResponse(request=request,name="sign-in")


@app.post("/sign-up")
def store_login_information(user_name: Annotated[str,Form()], password: Annotated[str,Form()], session: SessionDep):
    sign_up = Sign_Up(user_name=user_name, password=password)
    session.add(sign_up)
    session.commit()
    session.refresh(sign_up)

    return RedirectResponse(url=f"/create_portfolio/{user_name}", status_code=303)


'''Create Login Feature next in which user_id and password is authenticated from the database. First Search -> Username in the database
if found see if the password matches : if yes redirect to the create portfolio or edit portfolio '''


