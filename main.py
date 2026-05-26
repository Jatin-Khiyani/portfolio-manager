import json
from typing import Annotated
 
from fastapi import FastAPI, Form, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
 
from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, Session, select
 
from starlette.middleware.sessions import SessionMiddleware
 
 
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="yes")
 
templates = Jinja2Templates(directory="HTML")
 
 
class Sign_Up(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    user_name: str
    password: str
 
 
class Person(SQLModel, table=True):
    person_id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(foreign_key="sign_up.user_name")
    name: str
    email: str
    phone: str | None = None
    location: str | None = None
    linkedin: str | None = None
    github: str | None = None
    website: str | None = None
    summary: str | None = None
    # JSON strings for structured data
    skills: str | None = None        # JSON: ["Python", "FastAPI", ...]
    languages: str | None = None     # JSON: [{"lang": "French", "level": "Native"}, ...]
    experience: str | None = None    # JSON: [{"company":..,"role":..,"start":..,"end":..,"description":..}, ...]
    education: str | None = None     # JSON: [{"school":..,"degree":..,"start":..,"end":..,"subjects":..}, ...]
    projects: str | None = None      # JSON: [{"name":..,"tech":..,"description":..}, ...]
    certifications: str | None = None  # JSON: [{"title":..,"year":..}, ...]
    interests: str | None = None     # plain text
 
 
sqlite_file_name = "portfolio_manager.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
 
 
def create_db():
    SQLModel.metadata.create_all(engine)
 
 
def get_session():
    with Session(engine) as session:
        yield session
 
 
SessionDep = Annotated[Session, Depends(get_session)]
 
 
@app.on_event("startup")
def on_startup():
    create_db()
 
 
@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")
 
 
@app.get("/sign-up", response_class=HTMLResponse)
def sign_up_page(request: Request):
    return templates.TemplateResponse(request=request, name="sign-up.html")
 
 
@app.get("/sign-in", response_class=HTMLResponse)
def sign_in_page(request: Request):
    return templates.TemplateResponse(request=request, name="sign-in.html")
 
 
@app.post("/sign-up")
def store_login_information(
    user_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: SessionDep,
    request: Request,
):
    user = session.exec(select(Sign_Up).where(Sign_Up.user_name == user_name)).first()
    if user:
        return templates.TemplateResponse(
            name="sign-up.html", request=request,
            context={"error": "User name already exists"},
        )
    sign_up = Sign_Up(user_name=user_name, password=password)
    session.add(sign_up)
    session.commit()
    request.session["user_name"] = user_name
    return RedirectResponse(url="/create-portfolio", status_code=303)
 
 
@app.post("/sign-in")
def check_login_information(
    user_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: SessionDep,
    request: Request,
):
    sign_up = session.exec(
        select(Sign_Up).where(Sign_Up.user_name == user_name, Sign_Up.password == password)
    ).first()
    if sign_up:
        request.session["user_name"] = user_name
        return templates.TemplateResponse(
            name="sign-in.html", request=request,
            context={"success": True, "name": user_name},
        )
    return templates.TemplateResponse(
        name="sign-in.html", request=request,
        context={"error": "Could not find username and password, please try again"},
    )
 
 
@app.get("/create-portfolio", response_class=HTMLResponse)
def create_portfolio_page(request: Request, session: SessionDep):
    user_name = request.session.get("user_name")
    if not user_name:
        return RedirectResponse(url="/sign-in")
    person = session.exec(select(Person).where(Person.user_name == user_name)).first()
    # Parse JSON fields for template pre-filling
    person_data = None
    if person:
        person_data = {
            "name": person.name,
            "email": person.email,
            "phone": person.phone or "",
            "location": person.location or "",
            "linkedin": person.linkedin or "",
            "github": person.github or "",
            "website": person.website or "",
            "summary": person.summary or "",
            "interests": person.interests or "",
            "skills": json.loads(person.skills) if person.skills else [],
            "languages": json.loads(person.languages) if person.languages else [],
            "experience": json.loads(person.experience) if person.experience else [],
            "education": json.loads(person.education) if person.education else [],
            "projects": json.loads(person.projects) if person.projects else [],
            "certifications": json.loads(person.certifications) if person.certifications else [],
        }
    return templates.TemplateResponse(
        request=request, name="create-portfolio.html",
        context={"person": person_data}
    )
 
 
@app.post("/create-portfolio")
def store_person_data(
    request: Request,
    session: SessionDep,
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    portfolio_json: Annotated[str, Form()],  # all structured data as one JSON blob
    phone: Annotated[str, Form()] = "",
    location: Annotated[str, Form()] = "",
    linkedin: Annotated[str, Form()] = "",
    github: Annotated[str, Form()] = "",
    website: Annotated[str, Form()] = "",
    summary: Annotated[str, Form()] = "",
    interests: Annotated[str, Form()] = "",
):
    user_name = request.session.get("user_name")
    if not user_name:
        return RedirectResponse(url="/sign-in")
 
    data = json.loads(portfolio_json)
 
    person = session.exec(select(Person).where(Person.user_name == user_name)).first()
 
    fields = dict(
        name=name, email=email, phone=phone, location=location,
        linkedin=linkedin, github=github, website=website,
        summary=summary, interests=interests,
        skills=json.dumps(data.get("skills", [])),
        languages=json.dumps(data.get("languages", [])),
        experience=json.dumps(data.get("experience", [])),
        education=json.dumps(data.get("education", [])),
        projects=json.dumps(data.get("projects", [])),
        certifications=json.dumps(data.get("certifications", [])),
    )
 
    if person:
        for k, v in fields.items():
            setattr(person, k, v)
    else:
        person = Person(user_name=user_name, **fields)
        session.add(person)
 
    session.commit()
    session.refresh(person)
    return RedirectResponse(url="/portfolio", status_code=303)
 
 
@app.get("/portfolio", response_class=HTMLResponse)
def profile(request: Request, session: SessionDep):
    user_name = request.session.get("user_name")
    if not user_name:
        return RedirectResponse(url="/sign-in")
    person = session.exec(select(Person).where(Person.user_name == user_name)).first()
    person_data = None
    if person:
        person_data = {
            "name": person.name,
            "email": person.email,
            "phone": person.phone or "",
            "location": person.location or "",
            "linkedin": person.linkedin or "",
            "github": person.github or "",
            "website": person.website or "",
            "summary": person.summary or "",
            "interests": person.interests or "",
            "skills": json.loads(person.skills) if person.skills else [],
            "languages": json.loads(person.languages) if person.languages else [],
            "experience": json.loads(person.experience) if person.experience else [],
            "education": json.loads(person.education) if person.education else [],
            "projects": json.loads(person.projects) if person.projects else [],
            "certifications": json.loads(person.certifications) if person.certifications else [],
        }
    return templates.TemplateResponse(
        request=request, name="portfolio.html", context={"person": person_data}
    )