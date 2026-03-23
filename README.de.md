# Taski — Aufgabenverwaltung

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Deployed](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render&logoColor=white)

Eine Full-Stack-Webanwendung, bei der jeder Benutzer nur seine eigenen Aufgaben sieht.

🔗 **Live-Demo:** https://taski-ti1r.onrender.com
📄 **API documentation (Swagger):** https://taski-ti1r.onrender.com/apidocs

---

## Funktionen

- Registrierung und sicheres Einloggen
- Aufgaben erstellen mit Priorität (niedrig / mittel / hoch) und Fälligkeitsdatum
- Aufgaben als erledigt markieren oder löschen
- Jeder Benutzer sieht nur seine eigenen Aufgaben
- JWT-Authentifizierung — bleibt auch nach dem Schließen des Browsers eingeloggt

## Technologien

| Bereich | Technologie |
|---|---|
| Backend | Python, Flask |
| Authentifizierung | JWT, bcrypt |
| Datenbank | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |

## Lokale Installation

**1. Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

**2. Datenbank erstellen**
```bash
psql -U postgres -c "CREATE DATABASE taskmanager;"
psql -U postgres -d taskmanager -f schema.sql
```

**3. Umgebungsvariablen einrichten**
```bash
cp .env.example .env
# Eigene Werte eintragen
```

**4. Server starten**
```bash
python app.py
```

Anwendung öffnen unter `http://localhost:5000`

## Projektstruktur

```
├── app.py          # Routen und Aufgaben-Logik
├── auth.py         # Registrierung und Login
├── middleware.py   # JWT-Token-Überprüfung
├── db.py           # Datenbankverbindung
├── schema.sql      # Datenbanktabellen
└── templates/      # HTML-Seiten
```

## Screenshots
<img width="1920" height="938" alt="image" src="https://github.com/user-attachments/assets/794bad59-a60c-45aa-aa68-638f3bd8bbee" />

<img width="1920" height="939" alt="image" src="https://github.com/user-attachments/assets/c0703906-c5f9-4736-8ac2-dc962f2fe40b" />
