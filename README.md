# Portfolio Manager (FastAPI)

A minimal portfolio manager built with FastAPI.  
This project is in an early stage and currently supports basic profile creation and viewing.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Usage

### Add a Person

Go to:
http://127.0.0.1:8000/docs

Use the POST endpoint with:

```json
{
  "person_id": 0,
  "name": "string",
  "email": "string",
  "experience": "string",
  "education": "string",
  "projects": "string"
}
```

### View Data

- Home: http://127.0.0.1:8000/  
  Lists all people

- Profile: http://127.0.0.1:8000/{Name}  
  View full profile

## Current Features

- Add profiles via API
- List all users
- View individual profiles

## Status

Early development — no persistence, validation, or authentication yet.

