# 🎓 Futor — Find Trusted Tutors in Your Area

> A complete full-stack tutoring platform built with Django for a final-year college project.

---

## 📦 Tech Stack

| Layer      | Technology                              |
|------------|------------------------------------------|
| Backend    | Python 3.10+, Django 4.2, Django REST Framework |
| Database   | SQLite (dev)                            |
| Frontend   | HTML5, CSS3 (custom), Vanilla JavaScript |
| Fonts      | Sora + DM Sans (Google Fonts)           |
| Icons      | Font Awesome 6                          |
| Auth       | Django Custom User Model (email-based)  |

---

## 🚀 Setup Instructions

### Step 1 — Clone / Extract the project

```bash
cd futor
```

### Step 2 — Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install django djangorestframework pillow
```

### Step 4 — Apply migrations

```bash
python manage.py makemigrations accounts courses bookings reviews
python manage.py migrate
```

### Step 5 — Seed dummy data (optional but recommended)

```bash
python manage.py seed_data
```

This creates:
- 1 Admin account
- 6 Teacher accounts
- 4 Student accounts
- Sample bookings, reviews, courses, and favorites

### Step 6 — Run the development server

```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000**

---

## 🔐 Default Login Credentials (after seed_data)

| Role    | Email                | Password    |
|---------|----------------------|-------------|
| Admin   | admin@futor.in       | admin123    |
| Teacher | anita@futor.in       | teacher123  |
| Student | rahul@futor.in       | student123  |

Admin panel: **http://127.0.0.1:8000/admin/**

---

## 📁 Project Structure

```
futor/
├── futor/                  # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/               # Custom User, Login, Register, Profiles
│   ├── models.py           # CustomUser, TeacherProfile, StudentProfile
│   ├── views.py            # register, login, logout, role_select, profile
│   ├── forms.py            # UserRegistrationForm, LoginForm, ProfileForms
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── seed_data.py
│
├── home/                   # Landing page, About, Contact
├── courses/                # Course listing with class/subject selection
├── tutors/                 # Tutor listing & detail pages
├── dashboard/              # Student & Teacher dashboards
├── bookings/               # Demo class booking system
├── reviews/                # Rating & review system
│
├── templates/              # All HTML templates
│   ├── base.html           # Master layout (navbar, footer, alerts)
│   ├── home/
│   ├── accounts/
│   ├── courses/
│   ├── tutors/
│   ├── dashboard/
│   └── bookings/
│
├── static/
│   ├── css/main.css        # Complete custom CSS (design system)
│   └── js/main.js          # All JavaScript (dark mode, animations, etc.)
│
├── media/                  # User uploads (profile images, demo videos)
│   ├── profile_images/
│   └── demo_videos/
│
├── manage.py
└── README.md
```

---

## ✨ Features

### Frontend
- ✅ Fully responsive (Mobile, Tablet, Laptop, Desktop)
- ✅ Sticky navbar with hamburger menu (mobile)
- ✅ Hero typing animation (letter-by-letter)
- ✅ Dark / Light mode toggle (saved to localStorage)
- ✅ Scroll-to-top button
- ✅ CSS scroll-reveal animations
- ✅ FAQ accordion
- ✅ Subject search suggestions (live)
- ✅ Featured tutor cards with hover effects
- ✅ Testimonials and FAQ sections
- ✅ Page loading animation

### Backend / Django
- ✅ Custom User Model (email-based login)
- ✅ Role-based access: Student / Teacher
- ✅ Teacher & Student profile management
- ✅ Demo class booking system
- ✅ Booking status: Pending → Confirmed → Completed
- ✅ Star rating & review system
- ✅ Favorite tutors (per student)
- ✅ Dynamic course/subject filtering by class
- ✅ Tutor search by location, subject, mode, fees
- ✅ Profile image & demo video upload
- ✅ YouTube demo video link support
- ✅ CSRF protection throughout
- ✅ Custom Django admin panel
- ✅ Django messages framework (alerts)
- ✅ Dummy data seeder command

---

## 🗃️ Database Models

| Model           | Key Fields                                              |
|-----------------|---------------------------------------------------------|
| CustomUser      | email, full_name, phone, profile_image, role            |
| TeacherProfile  | qualification, experience, subjects, fees, city, mode   |
| StudentProfile  | class_name, subjects, city, favorite_tutors             |
| Course          | class_name, subject_name                               |
| Booking         | student, teacher, subject, date, time, status          |
| Review          | student, teacher, rating, review_text                   |

---

## 🎨 Color Palette

| Name          | Value     |
|---------------|-----------|
| Primary       | #1a2e4a   |
| Accent (Blue) | #0ea5e9   |
| Success       | #10b981   |
| Warning       | #f59e0b   |
| Danger        | #ef4444   |

---

## 📸 Adding Profile Images

Upload images via:
1. **Admin panel** → Users / Teacher Profiles
2. **Teacher Dashboard** → Edit Profile → Upload photo

Images are stored in `media/profile_images/`

---

## 🔧 Common Commands

```bash
# Create admin
python manage.py createsuperuser

# Make & apply migrations
python manage.py makemigrations
python manage.py migrate

# Seed dummy data
python manage.py seed_data

# Collect static files (for production)
python manage.py collectstatic
```

---

## 📋 App URL Structure

| URL                        | View                        |
|----------------------------|-----------------------------|
| `/`                        | Home page                   |
| `/accounts/register/`      | Registration                |
| `/accounts/login/`         | Login                       |
| `/accounts/logout/`        | Logout                      |
| `/accounts/role-select/`   | Student / Teacher selection |
| `/accounts/profile/`       | Profile edit                |
| `/courses/`                | Course browser              |
| `/tutors/`                 | Tutor listing               |
| `/tutors/<id>/`            | Tutor detail                |
| `/dashboard/student/`      | Student dashboard           |
| `/dashboard/teacher/`      | Teacher dashboard           |
| `/bookings/book/<id>/`     | Book demo class             |
| `/reviews/add/<id>/`       | Add review                  |
| `/admin/`                  | Django admin                |

---

