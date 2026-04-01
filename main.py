from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 


app = FastAPI()

people_db = []

templates = Jinja2Templates(directory="templates") 
welcome_msg = "Profile for user"
class Person(BaseModel):
    person_id: int
    name: str
    profession : str
    experience: str
    education: str


@app.post("/people")
def add_person(person: Person):
    people_db.append(person.dict()) 
    return {
        "message": "Person added successfully",
        "data": person
    }

@app.get("/people")
def get_all_people():
    return people_db


@app.get("/", response_class=HTMLResponse)
def get_HTML(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "people": people_db,  
            "welcome_message": welcome_msg
        }
    )

# @app.get("/people/{person_id}/profile", response_class=HTMLResponse)
# def get_person_profile(person_id: int):
#     if person_id in people_db:
#         person = people_db[person_id]
#         return templates.TemplateResponse("profile.html", {"request": {}, "person": person})
#     return {"error": "Person not found"}

@app.get("/people/{person_id}")
def get_person(person_id: int):
    for person in people_db:
        if person["person_id"] == person_id:
            return person
    return {"error": "Person not found"}