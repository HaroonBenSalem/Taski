🇩🇪 [Auf Deutsch lesen](README.de.md)
# Taski — Task Manager

A full-stack task manager where every user sees only their own tasks.

🔗 **Live demo:** https://taski-ti1r.onrender.com

---

## Features

- Register and log in securely
- Add tasks with priority (low / medium / high) and due date
- Mark tasks as done or delete them
- Each user sees only their own tasks
- JWT authentication — stays logged in across sessions

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, Flask |
| Auth | JWT, bcrypt |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |

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
