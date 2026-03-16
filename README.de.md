# Taski — Aufgabenverwaltung

Eine Full-Stack-Webanwendung, bei der jeder Benutzer nur seine eigenen Aufgaben sieht.

🔗 **Live-Demo:** https://taski-ti1r.onrender.com

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
