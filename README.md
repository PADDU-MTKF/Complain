# 🛠️ Complaint Management System – Backend API

A **Django REST Framework–based backend service** designed to handle **user authentication, complaint registration, progress tracking, and media uploads**, using **Appwrite Database and Storage** as the backend data layer.

This project focuses on building a **secure, modular, and scalable API** that can be consumed by web or mobile applications.


---

## 📌 Project Overview

The Complaint Management System allows users to:

- Register and authenticate securely
- Raise complaints with image evidence
- Track complaint progress
- Allow authorized roles to manage complaint status
- Store structured data and files using **Appwrite**

The backend follows a **stateless API architecture** with **TOKEN-based authentication**, making it suitable for integration with any frontend stack.

---

## ✨ Key Features
- Secure username & password authentication  
- TOKEN-based authorization for protected endpoints  
- User profile management (create, view, update, delete)  
- Role-based user access (user / staff / admin)    
- Support for uploading up to **3 images per complaint**  
- Image storage using **Appwrite Storage**  
- Track and update complaint progress/status  
- Fetch complaints globally or user-wise  
- Automatic media cleanup on complaint deletion    
- Pagination support for listing complaints  


## 🔄 Application Flow

1. **User registers** via API
2. **User logs in** and receives TOKEN
3. TOKEN is passed in request headers
4. User creates complaint with image evidence
5. Complaints are stored in Appwrite Database
6. Images are stored in Appwrite Storage
7. Authorized roles update complaint progress
8. Complaints can be deleted along with media

---


## 🔐 Security Notes

- Passwords are stored securely and **never exposed**
- All sensitive endpoints require:
  - `TOKEN`
  - `USERNAME` (where applicable)
- Invalid or expired tokens block access
- Image upload permissions enforced via backend

---

## 🛠️ Tech Stack
<p align="left">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="32" />
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" width="32" />
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/appwrite/appwrite-original.svg" width="32" />
</p>

- **Python**
- **Django REST Framework**
- **Appwrite** (Database & Storage)


---

## 📦 Deployment Notes

- Can be deployed on any VPS or cloud server
- Compatible with:
  - Gunicorn
  - Nginx
  - Docker
- Requires Appwrite instance (cloud or self-hosted)

---

## 🔗 API Endpoints

### 🔐 Authentication

| Method | Endpoint | Auth Required | Description |
|------|---------|--------------|-------------|
| POST | `/login` | ❌ No | Authenticate user and return TOKEN |

---

### 👤 User Management

| Method | Endpoint | Auth Required | Description |
|------|---------|--------------|-------------|
| GET | `/user?username=` | ✅ TOKEN | Get user profile details |
| POST | `/user` | ❌ No | Create new user account |
| PUT | `/user` | ✅ TOKEN | Update user profile |
| DELETE | `/user` | ✅ TOKEN | Delete user account |
| PUT | `/user/role` | ✅ TOKEN | Update user role (admin/staff) |

---

### 📣 Complaint Management

| Method | Endpoint | Auth Required | Description |
|------|---------|--------------|-------------|
| GET | `/complain?page=` | ❌ No | Fetch all complaints (paginated) |
| GET | `/complain?username=` | ❌ No | Fetch complaints by username |
| POST | `/complain` | ✅ TOKEN | Create a new complaint with images |
| PUT | `/complain` | ✅ TOKEN | Update complaint progress/status |
| POST | `/complain/delete` | ✅ TOKEN | Delete complaint and images |

---

