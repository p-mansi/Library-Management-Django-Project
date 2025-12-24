# 📚 Library Management System (Django)

A **role-based Library Management System** built using **Django** that allows admins and librarians to manage books, and members to browse, borrow, review, and wishlist books. The system includes authentication, authorization, reviews, email reminders, and recommendations.

---

## 🚀 Features

### 👥 User Roles

* **Admin**
* **Librarian**
* **Member**

Each role has different permissions and access levels.

---

### 📖 Book Management

* Add, update, delete books (Admin / Librarian)
* Upload book cover images
* Assign genres to books
* Track availability status

---

### 🔄 Borrow & Return

* Members can borrow available books
* Due date tracking
* Return books functionality
* Prevent duplicate borrowing

---

### ⭐ Reviews & Ratings

* Members can add or edit reviews (1–5 stars)
* One review per user per book
* View all reviews for a book
* Average rating calculation

---

### ❤️ Wishlist

* Add books to wishlist
* Remove books from wishlist
* Personalized wishlist view

---

### 📊 Dashboard & Profile

* Admin dashboard with:

  * Total books
  * Borrowed books
  * Overdue books
  * Active members
* User profile with:

  * Borrow history
  * Review count

---

## 🛠 Tech Stack

* **Backend:** Django, Python
* **Database:** SQLite (default)
* **Frontend:** HTML, CSS, Bootstrap, JavaScript
* **Authentication:** Django Auth
* **ORM:** Django ORM

---

## 📂 Project Structure

```
casestudy_project/
│
├── Books/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── utils.py
│   ├── urls.py
│   └── apps.py
│
├── static/
├── media/
├── templates/
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/username/library-management-system.git
cd library-management-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 6️⃣ Run Server

```bash
python manage.py runserver
```

Access the app at:
👉 `http://127.0.0.1:8000/`

---

## 🔐 Default Roles

* **Admin:** Full access
* **Librarian:** Manage books & borrowing
* **Member:** Browse, borrow, review, wishlist

Roles are assigned during registration.

---

## 🧪 Testing

* Admin panel testing
* Role-based access testing
* Borrow/Return flow tested
* JSON-based review API tested

---

## 📌 Design Assumptions

* One user can review a book only once
* Members can borrow only available books
* Books become unavailable once borrowed
* SQLite used for simplicity (can switch to PostgreSQL)

---

## 📈 Future Enhancements

* Fine calculation for overdue books
* PDF/Excel report export
* REST API with Django REST Framework
* Payment gateway for fines
* React frontend integration

---

## 👩‍💻 Author

**Mansi**
MCA Student | Java & Django Developer
GitHub: [https://github.com/p-mansi](https://github.com/p-mansi)

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it motivates a lot!
