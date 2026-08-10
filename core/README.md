# 🎓 MEDINIPUR PLATFORM

A full-stack web application built with **Django** designed to connect students with qualified teachers and Mess/PG accommodations across Medinipur.

Developed and maintained by **Mithun Patra** (Astronomy & Space Researcher, NISER, India).

---

## 🚀 Features

### 👨‍🏫 Teacher / Tutor Directory
- **Browse Tutors:** View registered tutors with detail cards and verification tags.
- **Search & Filter:** Filter tutors by level, class, district, and subject.
- **Teacher Registration:** Easy registration form for teachers to list their profile.
- **Excel Sync:** Auto-syncs registered teacher records to a local spreadsheet (`teachers.xlsx`).
- **Profile Security:** Phone verification mechanism required for editing or deleting listings.

### 🏠 Mess & PG Listings
- **Accommodation Directory:** Browse student stays, boys/girls PGs, and messes.
- **Property Listing:** Simple form for property owners to list rent, food availability, and contact numbers.
- **Dynamic Views:** Track property engagement with direct database view incrementing.

---

## 📁 Project Structure

```text
MEDINIPUR_PLATFORM/
│
├── core/                        # Main application logic
│   ├── templates/               # HTML template files
│   │   ├── add_messpg.html
│   │   ├── add_teacher.html
│   │   ├── delete_confirm.html
│   │   ├── home.html
│   │   ├── messpg_list.html
│   │   ├── teacher_detail.html
│   │   └── teachers_list.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                # Teacher and MessPG models
│   ├── PROJECT_REVIEW.txt       # Weekly maintenance log & review checklist
│   ├── tests.py
│   ├── urls.py                  # Core routing
│   └── views.py                 # Request processing & search filtering
│
├── Flowchart/                   # Architecture & design diagrams
│   └── Version1.0.png
│
├── medinipur_platform/          # Django project configuration
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .vscode/                     # VS Code workspace settings
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django CLI management script
└── README.md