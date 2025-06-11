
# 📱 TableTap – Digital Menu & Subscription Management Platform

**TableTap** is a Django-based SaaS web platform designed for restaurants and cafes to manage their digital menus, streamline customer ordering via QR codes, and handle vendor subscriptions. With an intuitive admin panel and vendor dashboard, TableTap enables easy menu creation, item management, and real-time customer interaction at tables.

---

## 🚀 Features

- 🧾 **Vendor Authentication**  
  Secure sign-up, login, and dashboard for vendors

- 🗂️ **Menu & Item Management**  
  Create categories, add food/drink items with images, descriptions, and prices

- 📲 **QR Code Table Assignment**  
  Generate unique QR codes linked to individual vendor tables for customer ordering

- 🛒 **Customer Cart & Ordering System**  
  Customers can browse, add items to cart, and place orders—no login required

- 💼 **Subscription Controls**  
  SaaS-style subscription features: enable, pause, or archive vendor access

- ⚙️ **Django Admin Panel**  
  Superusers can manage vendor accounts, subscriptions, and data from a central interface

---

## 🛠️ Tech Stack

| Component   | Technology |
|-------------|------------|
| **Backend** | Django 5.1.7 |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | SQLite (default), supports PostgreSQL for production |
| **Media Handling** | Django `ImageField` with `MEDIA_URL` and `MEDIA_ROOT` |
| **QR Code** | Python `qrcode` library (or Django-compatible QR generator) |
| **Authentication** | Django's built-in user auth for vendor login and access control |

---

## 🧠 Use of Generative AI

Generative AI tools were used as **assistants** to improve productivity and enhance the quality of both backend and frontend code during development.

### AI-Assisted Development Included:

- 🧩 **Debugging Django view/template errors**
- 🎨 **Enhancing frontend styling and layout using CSS**
- 📄 **Improving readability and structure of code documentation**
- 🔄 **Speeding up development with iterative UI and form logic suggestions**

### Tools Used:

- [OpenAI GPT-4o](https://openai.com/) – for Django model/view logic, form handling, admin customizations  
- [Claude 3.5 Sonnet](https://www.anthropic.com/index/claude-3-5) – for layout and CSS fine-tuning

> ⚠️ AI suggestions were manually reviewed and verified before integration.

---

## 🔐 Admin Access

Admin users (superusers) can:
- Manage all vendor accounts
- Create, pause, or archive subscriptions
- View customer orders and menu structures
- Access advanced filtering and search in the Django admin

To create a superuser:
```bash
python manage.py createsuperuser
```

---

## 🧪 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/tabletap.git
cd tabletap
```

### 2. Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=tabletap_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply Migrations and Run

```bash
python manage.py migrate
python manage.py runserver
```

---

## 📁 Project Structure

```
tabletap/
├── tabletap/         # Main Django settings and wsgi
├── tableapp/         # App for menu/items logic
├── media/            # Uploaded item images
├── env/              # Virtual environment (excluded from Git)
├── manage.py         # Django entry point
├── db.sqlite3        # Default development DB
└── .env              # Environment variables file
```

---

## 📬 Contact

For questions or collaboration, feel free to reach out at [your-email@example.com]

---

© 2025 TableTap. All rights reserved.
