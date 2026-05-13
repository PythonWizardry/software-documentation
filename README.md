# software-documentation
This repository contains my lab assignments for the course "Software Documentation and Design Patterns"


## Software Documentation - Lab 3 (MVC Web App)

Main entity for MVC part: **Application** (Google Play Store domain).

Implemented according to assignment:

- MVC controllers (FastAPI routes) for Application entity
- Model and DB interaction through SQLAlchemy + repository
- Business logic layer is used by controllers for data read/write
- CRUD operations: create, read, update, delete
- HTML views rendered with Jinja2 templates

### MVC Routes

- GET `/` -> redirect to applications page
- GET `/applications` -> list applications (HTML)
- GET `/applications/create` -> create form (HTML)
- POST `/applications/create` -> create application
- GET `/applications/{app_id}` -> details page (HTML)
- GET `/applications/{app_id}/edit` -> edit form (HTML)
- POST `/applications/{app_id}/edit` -> update application
- POST `/applications/{app_id}/delete` -> delete application

### Run MVC App

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run server:

```bash
uvicorn api:app --reload
```

### Google Login (Firebase)

This lab requires Google login via Firebase. Configure these environment variables before running the app:

- `SESSION_SECRET_KEY` - random string for session signing.
- `FIREBASE_CREDENTIALS` - path to Firebase service account JSON file.
- `FIREBASE_WEB_CONFIG` - Firebase web config JSON string (from Firebase Console).

Example (PowerShell):

```powershell
$env:SESSION_SECRET_KEY = "change-this"
$env:FIREBASE_CREDENTIALS = "C:\path\to\serviceAccount.json"
$env:FIREBASE_WEB_CONFIG = '{"apiKey":"...","authDomain":"...","projectId":"...","appId":"..."}'
```

3. Open browser:

- MVC pages: http://127.0.0.1:8000/applications

## Notes

- Database file is created locally as SQLite.
