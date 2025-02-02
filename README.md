# Role-Based Authentication System

## 📌 Project Overview
This is a **Role-Based Authentication System** built using Django and Django REST Framework (DRF). It provides user authentication, role-based access control (RBAC), JWT authentication, and API endpoints for user management. Additionally, it includes **password hashing using bcrypt** and **forgot password functionality**.

## 🚀 Features
- **User Registration & Authentication** (JWT-based)
- **Role-Based Access Control (RBAC)** (Student, Parent, School)
- **Secure Password Hashing** using `bcrypt`
- **Forgot Password & Reset Password** via email
- **Student Dashboard** (Achievements & Profile)
- **Parent Dashboard** (Monitor child's achievements)
- **School Dashboard** (Manage students)
- **CRUD Operations** for user roles & achievements

## 🏗️ Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL / MySQL
- **Authentication**: JWT (Django Simple JWT)
- **Security**: bcrypt for password hashing

## 🔧 Installation & Setup
### 1️⃣ Clone the repository:
```bash
git clone https://github.com/mohitmahur/slate-backend.git
cd slate-backend
```

### 2️⃣ Create a virtual environment & activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

### 4️⃣ Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a superuser:
```bash
python manage.py createsuperuser
```

### 6️⃣ Start the development server:
```bash
python manage.py runserver
```

## 🔑 API Endpoints
### Authentication APIs:
| Method | Endpoint | Description |
|--------|-------------|----------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login & get JWT tokens |
| POST | `/api/auth/forgot-password/` | Request password reset |
| POST | `/api/auth/reset-password/` | Reset password |

### Dashboard APIs:
| Method | Endpoint | Description |
|--------|-------------|----------------|
| GET | `/api/dashboard/student/` | Student dashboard |
| GET | `/api/dashboard/parent/` | Parent dashboard |
| GET | `/api/dashboard/school/` | School dashboard |

### Achievements API:
| Method | Endpoint | Description |
|--------|-------------|----------------|
| GET | `/api/student/achievements/<int:student_id>/` | View student achievements |
| POST | `/api/achievements/` | Add new achievement |

## 🔒 Security Enhancements
- **bcrypt password hashing** for enhanced security
- **JWT authentication** for secure API access
- **Role-Based Access Control (RBAC)** to restrict unauthorized access

## 📜 License
This project is open-source and available under the **MIT License**.

## 🤝 Contributing
Feel free to **fork** this repository and submit **pull requests**. Suggestions & improvements are always welcome!

## 📬 Contact
For queries or collaborations, reach out at **your-email@example.com**.

---
⭐ **If you like this project, don't forget to star the repository!** ⭐

