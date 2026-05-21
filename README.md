# Portfolio Manager

A web app where users sign up, enter their professional details, and get a clean printable resume. Built with FastAPI, SQLModel, and Jinja2 templates.

---

## Stack

FastAPI · SQLModel · SQLite · Jinja2 · HTML/CSS · Uvicorn

---

## Setup

Requires Python 3.10.4 — the app breaks on higher versions.

```bash
python --version
# Python 3.10.4
```

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

App runs at http://127.0.0.1:8000

---

## How it works

Sign up or sign in, fill in your name, email, experience, education, and projects, and the app generates a formatted resume page at `/portfolio`.

---

## Known Issues

- After logging in, the existing portfolio is not fetched from the database — users have to re-enter their details, and each submission creates a duplicate entry
- Passwords are stored in plain text with no hashing

---

## Planned Features

- Fetch existing portfolio on login and prevent duplicate entries
- Password hashing with bcrypt/passlib
- Edit portfolio details directly from the portfolio page
- Export resume as a PDF
- More resume fields — multiple experience entries, skills, project cards, social links
