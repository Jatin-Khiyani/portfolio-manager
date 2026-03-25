from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

people_db = {}


class Person(BaseModel):
    person_id: int
    name: str
    profession : str
    phone_no: int
    email: str
    summary: str


@app.post("/people")
def add_person(person: Person):
    people_db[person.person_id] = person
    return {
        "message": "Person added successfully",
        "data": person
    }

@app.get("/people")
def get_all_people():
    return people_db

@app.get("/people/{person_id}")
def get_person(person_id: int):
    if person_id in people_db:
        return people_db[person_id]
    return {"error": "Person not found"}
