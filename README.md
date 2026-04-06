# 📄 Resume Builder

A full-stack Django web application that lets users register, fill in their academic and professional profile, and instantly generate a formatted PDF resume — all from the browser.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## ✨ Features

- User registration and login system
- Profile builder — education, skills, projects, career objective, work experience
- One-click PDF resume generation using ReportLab
- Admin dashboard for managing users and job notifications
- Notification board for job postings
- Profile photo upload support

---

## 🏗️ Architecture

```
Browser (HTML/CSS)
       │
       ▼
  Django Views  ──────────────────────────────┐
       │                                       │
       ▼                                       ▼
  Django ORM                            ReportLab PDF
       │                                  Generator
       ▼                                       │
   SQLite DB                                   ▼
(User Profiles,                        PDF File Download
 Notifications)                          ← returned to browser
```

### Request Flow

```
User fills form
      │
      ▼
POST request → Django View validates form data
      │
      ▼
UserModel saved to SQLite via Django ORM
      │
      ▼
User clicks "Generate Resume"
      │
      ▼
Django fetches profile from SQLite
      │
      ▼
ReportLab draws PDF layout (name, education, skills, projects)
      │
      ▼
PDF returned as file download to browser
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3 |
| Web Framework | Django |
| Database | SQLite |
| PDF Generation | ReportLab |
| Frontend | HTML, CSS (Django Templates) |
| Admin Panel | Django Admin |

---

## 📁 Project Structure

```
ResumeBuilder/
├── manage.py                  # Django entry point
├── ResumeBuilder/
│   ├── settings.py            # Project settings
│   ├── urls.py                # Root URL config
│   ├── wsgi.py
│   └── asgi.py
├── resume/
│   ├── models.py              # UserModel, NotificationModel
│   ├── views.py               # All view logic + PDF generation
│   ├── forms.py               # Registration and login forms
│   ├── admin.py               # Admin panel config
│   ├── constants.py
│   └── migrations/            # Database migrations
├── templates/
│   ├── index.html             # Login page
│   ├── registration.html      # Register page
│   ├── users.html             # User profile page
│   ├── viewprofile.html       # View/edit profile
│   ├── viewnotifications.html # Job notifications
│   └── addnotification.html   # Admin: add notification
└── static/                    # CSS and static assets
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.6+
- Conda (recommended) or pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ajay062002/resume-builder.git
cd resume-builder

# 2. Create and activate environment
conda create -n resumebuilder python=3.8
conda activate resumebuilder

# 3. Install dependencies
pip install django reportlab pillow

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (for admin access)
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Then open your browser at `http://127.0.0.1:8000`

---

## 🚀 How to Use

### As a User
1. Go to `http://127.0.0.1:8000` and register an account
2. Fill in your profile — education, skills, projects, career objective
3. Upload a profile photo
4. Click **Generate Resume** to download your PDF resume

### As an Admin
1. Go to `http://127.0.0.1:8000/admin`
2. Login with superuser credentials
3. Manage users, view profiles, and post job notifications

---

## 📊 Database Models

### UserModel
Stores the complete user profile including personal info, education percentages, skills, projects, career objective, and profile photo.

### NotificationModel
Stores job postings created by the admin — title, description, required skills, and date.

---

## 🔮 Future Improvements

- Multiple resume templates to choose from
- Export to DOCX format
- Online resume sharing via unique link
- Real-time preview before download
- Cloud storage for profile photos

---

## 👤 Author

**Ajay Thota**
- GitHub: [@ajay062002](https://github.com/ajay062002)
- Portfolio: [ajaylive.com](https://ajaylive.com)
