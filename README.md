# Resume Builder

A Django web app where students fill in their profile and download a formatted PDF resume. Admins post job notifications and search candidates ranked by skill match.

---

## What it does

**Students** register, fill in five profile tabs (Personal, Education, Skills, Projects, Experience), and download a clean PDF resume generated server-side from their data.

**Admins** log in to post job notifications with required skills, and search the candidate pool — results are ranked by how many required skills each student matches.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Django |
| Frontend | React (in-browser Babel), HTML/CSS |
| Database | SQLite |
| PDF generation | ReportLab (Platypus layout engine) |
| Static files | WhiteNoise |

---

## Project Structure

```
resume-builder/
├── ResumeBuilder/          # Django project config
│   ├── settings.py
│   ├── settings_prod.py
│   └── urls.py
│
├── resume/                 # Main app
│   ├── models.py           # UserModel, NotificationModel
│   ├── forms.py
│   │
│   ├── views/              # Template-based views
│   │   ├── auth.py         # registration, login, logout
│   │   ├── profile.py      # viewprofile, updateprofile, updatepic
│   │   ├── search.py       # admin skill search
│   │   ├── notifications.py
│   │   └── download.py     # PDF download
│   │
│   ├── api/                # JSON API (used by React frontend)
│   │   ├── auth.py         # /api/login/ /api/logout/ /api/register/
│   │   ├── profile.py      # /api/profile/ /api/profile/update/ /api/download/
│   │   ├── search.py       # /api/search/
│   │   └── notifications.py
│   │
│   └── pdf/                # PDF generation
│       ├── styles.py       # ReportLab ParagraphStyle definitions
│       ├── sections.py     # One function per resume section
│       └── builder.py      # build_resume_pdf(user) -> returns file path
│
├── static/
│   └── resume-ranking.html # React SPA (main UI)
├── templates/              # Django HTML templates
├── generated/              # Generated PDF output
└── images/                 # Uploaded profile photos
```

---

## Running Locally

```bash
git clone https://github.com/ajay062002/resume-builder.git
cd resume-builder
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://localhost:8000

Default admin: `admin` / `admin`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/csrf/` | Get CSRF cookie |
| POST | `/api/login/` | Login |
| POST | `/api/logout/` | Logout |
| POST | `/api/register/` | Register student |
| GET | `/api/profile/` | Get profile |
| POST | `/api/profile/update/` | Update profile |
| POST | `/api/profile/pic/` | Upload photo |
| GET | `/api/download/` | Download PDF resume |
| GET | `/api/search/?keyword=python,django` | Skill search (admin) |
| GET | `/api/notifications/` | List notifications |
| POST | `/api/notifications/add/` | Add notification (admin) |
| DELETE | `/api/notifications/<id>/delete/` | Delete notification (admin) |
