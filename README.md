# IFP Management System

The IFP (Industry-Focused Project) Management System is a web-based application developed using Python and Flask. It helps manage and streamline project details, student and faculty assignments, progress tracking, and approvals for academic institutions.

---

## 📁 Project Structure

```
projlast/
│
├── app.py                   # Main Flask application
├── instance/db.sqlite3     # SQLite database
├── alembic/                # Alembic migration environment
├── migrations/             # Database migration scripts
│   └── versions/           # Auto-generated migration files
└── templates/ & static/    # (Assumed to exist: HTML, CSS, JS files for frontend)
```

---

## 🚀 Features

- User roles: Admin, Student, Faculty
- Add/view/update IFP project titles
- Assign faculty guides to students
- Track project progress and approvals
- Database migrations with Alembic
- SQLite for local database storage

---

## 🔧 Technologies Used

- **Backend:** Python, Flask
- **Database:** SQLite
- **Migrations:** Alembic
- **Frontend:** HTML/CSS/JS (assumed in templates folder)

---

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd projlast
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   flask db upgrade
   ```

5. **Start the Flask application**
   ```bash
   python app.py
   ```

6. Open your browser and go to `http://127.0.0.1:5000/`

---


## 📝 License

This project is for academic and learning purposes.

---

## 🙌 Acknowledgements

Special thanks to the project mentors and contributors involved in the development of this system.
