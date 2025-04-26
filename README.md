# Business Management System

## Overview
A full-featured business management system designed for small businesses, combining:

- **Clients Management** — Manage clients, including general and inactive clients.
- **Projects Management** — Track client-related projects with deadlines and team assignments.
- **Tasks Management** — Manage tasks linked to projects, assigned to specific employees.
- **Inventory Management** — Manage stock items, automatic reduction after sales, track inventory transactions.
- **Invoices Management** — Create and manage client invoices, automatic calculation of total amounts.
- **Point of Sale (POS)** — Handle fast sales with inventory updates, manual or client-assigned sales.
- **Expenses Management** — Track business expenses and view monthly summaries.
- **Admin Dashboard** — View key statistics, financial overview, upcoming tasks, and recent activity.

---

## Features
- **Role-Based Access Control** (Admin, Manager, Employee)
- **Secure Views** with proper decorators and role checks
- **Automatic Inventory Adjustment** during sales and invoice creation
- **Professional UI/UX** built with Bootstrap 5
- **Activity Feed** showing latest actions
- **Upcoming Tasks** section
- **Sales and Invoices Filtering**
- **Mobile-friendly** and responsive design
- **Soft Deletes** for critical data (no loss of data)

---

## Technology Stack
- Python 3.10+
- Django 4.2+
- Bootstrap 5
- SQLite3 (for development)
- Gunicorn (for production)
- WhiteNoise (static files handling)
- HTML5 / CSS3 / JS

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
Create a virtual environment and activate it:

bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file:

env
Copy
Edit
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
Run migrations:

bash
Copy
Edit
python manage.py migrate
Create a superuser:

bash
Copy
Edit
python manage.py createsuperuser
Start the development server:

bash
Copy
Edit
python manage.py runserver
Deployment to Production
Environment Preparation
Add a proper .env file with production values (set DEBUG=False).

Use a PostgreSQL database (recommended for production).

Collect static files:

bash
Copy
Edit
python manage.py collectstatic
Deploy to Platforms
Heroku / Railway / Render / PythonAnywhere:

Make sure you have:

Procfile

runtime.txt

requirements.txt

LICENSE

Updated settings.py with environment variables (using python-decouple).

Basic deployment flow (example for Railway):

Push to GitHub.

Connect Railway to GitHub repository.

Set environment variables (.env) on the platform.

Deploy 🚀

Screenshots
(Add screenshots here in the future for better documentation)

License
This project is licensed under the MIT License.
See the LICENSE file for details.

