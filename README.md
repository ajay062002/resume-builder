# Resume Builder – Student & Recruiter Portal

A Django web app that connects students and recruiters. Students build their profile and download a generated PDF resume. Recruiters post job notifications and search candidates ranked by skill match.

---

## How It Works

**Student side**
- Register with personal info, education history, skills, projects, and work experience
- View and update your profile at any time
- Download a formatted PDF resume generated from your profile (via ReportLab)

**Recruiter / Admin side**
- Login as admin to access the recruiter dashboard
- Post job notifications with required skills and description
- Search students by skills — results are ranked by how many required skills each student matches
- View full candidate profiles and download their resumes

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Django |
| Database | SQLite (Django default) |
| PDF Generation | ReportLab |
| Frontend | HTML / CSS (Django templates) |
| Auth | Django session-based authentication |

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/ajay062002/resume-builder.git
cd resume-builder
```

### 2. Install dependencies
```bash
pip install django reportlab
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Start the server
```bash
python manage.py runserver
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## Login

| Role | Username | Password |
|------|----------|----------|
| Admin / Recruiter | `admin` | `admin` |
| Student | your registered email | your password |

---

## Features

- Student registration and profile management
- PDF resume generation with personal info, education, skills, projects, and experience
- Admin dashboard to post and manage job notifications
- Skill-based candidate search with match ranking
- Profile photo upload

---

## Author

[Ajay Thota](https://github.com/ajay062002)
