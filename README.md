# Portfolio Manager

A web-based portfolio manager built with **FastAPI**, **SQLModel**, and **Jinja2**. Users can sign up, sign in, and generate a clean, printable one-page resume from their profile details.

---

## Requirements

- **Python 3.10.4** (strictly required)
- pip
- Git (optional, for cloning)

---

## Setup

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd portfolio-manager
```

Or simply place all project files in a folder and navigate to it.

---

### 2. Create a virtual environment

A virtual environment isolates your project dependencies from the rest of your system. Make sure you are using Python 3.10.4 specifically.

#### macOS / Linux

```bash
python3.10 --version          # confirm it shows 3.10.4
python3.10 -m venv venv
source venv/bin/activate
```

#### Windows (Command Prompt)

```cmd
py -3.10 --version            :: confirm it shows 3.10.4
py -3.10 -m venv venv
venv\Scripts\activate.bat
```

#### Windows (PowerShell)

```powershell
py -3.10 --version            # confirm it shows 3.10.4
py -3.10 -m venv venv
venv\Scripts\Activate.ps1
```

> **Note:** If `python3.10` or `py -3.10` is not found, download Python 3.10.4 from [python.org](https://www.python.org/downloads/release/python-3104/) and ensure it is added to your PATH during installation.

---

### 3. Install dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

---

### 4. Project structure

Ensure your project folder looks like this before running:

```
portfolio-manager/
├── main.py
├── requirements.txt
├── portfolio_manager.db        # auto-created on first run
└── HTML/
    ├── home.html
    ├── sign-up.html
    ├── sign-in.html
    ├── create-portfolio.html
    └── portfolio.html
```

> The `HTML/` directory must contain all template files. The database file is created automatically on startup.

---

### 5. Run the development server

```bash
uvicorn main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

## Usage

| Page | URL | Description |
|---|---|---|
| Home | `http://127.0.0.1:8000/` | Landing page with sign up / sign in links |
| Sign Up | `http://127.0.0.1:8000/sign-up` | Create a new account |
| Sign In | `http://127.0.0.1:8000/sign-in` | Log in to an existing account |
| Create Portfolio | `http://127.0.0.1:8000/create-portfolio` | Fill in your resume details |
| Portfolio | `http://127.0.0.1:8000/portfolio` | View your generated resume |
| API Docs | `http://127.0.0.1:8000/docs` | Interactive Swagger UI for the API |

---

## Features

- User authentication (sign up and sign in)
- Session-based login state
- Portfolio creation form (name, email, experience, education, projects)
- Clean, printable one-page resume output
- SQLite database with SQLModel ORM
- Jinja2 HTML templating

---

## Deactivating the virtual environment

When you are done, deactivate the environment with:

```bash
deactivate
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI | Web framework |
| SQLModel | ORM and database models |
| SQLite | Database |
| Jinja2 | HTML templating |
| Starlette Sessions | Session middleware |
| Uvicorn | ASGI server |
