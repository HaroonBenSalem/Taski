🇩🇪 [Auf Deutsch lesen](README.de.md)

# Taski — Task Manager

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Deployed](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render&logoColor=white)

A full-stack task manager where every user sees only their own tasks.

🔗 **Live demo:** https://taski-ti1r.onrender.com
📄 **API documentation (Swagger):** https://taski-ti1r.onrender.com/apidocs

---

## Features

- Register and log in securely
- Add tasks with priority (low / medium / high) and due date
- Mark tasks as done or delete them
- Each user sees only their own tasks
- JWT authentication — stays logged in across sessions
- REST API with full Swagger / OpenAPI documentation

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, Flask |
| Auth | JWT, bcrypt |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| API Docs | Flasgger (Swagger UI) |
| Deployment | Render |

## API Endpoints

Full interactive documentation available at [`/apidocs`](https://taski-ti1r.onrender.com/apidocs)

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register` | Create a new account | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/tasks` | Get all tasks | Yes |
| POST | `/tasks` | Create a new task | Yes |
| POST | `/tasks/<id>/done` | Toggle task done/undone | Yes |
| DELETE | `/tasks/<id>` | Delete a task | Yes |

## Run Locally

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Create the database**
```bash
psql -U postgres -c "CREATE DATABASE taskmanager;"
psql -U postgres -d taskmanager -f schema.sql
```

**3. Set up environment variables**
```bash
cp .env.example .env
# Fill in your values
```

**4. Start the server**
```bash
python app.py
```

Open `http://localhost:5000`
Open `http://localhost:5000/apidocs` for API documentation

## Project Structure

```
├── app.py          # Routes and task logic
├── auth.py         # Register and login endpoints
├── middleware.py   # JWT token verification
├── db.py           # Database connection
├── schema.sql      # Database tables
└── templates/      # HTML pages
```

## Screenshots

<img width="1920" height="938" alt="image" src="https://github.com/user-attachments/assets/794bad59-a60c-45aa-aa68-638f3bd8bbee" />

<img width="1920" height="939" alt="image" src="https://github.com/user-attachments/assets/c0703906-c5f9-4736-8ac2-dc962f2fe40b" />
