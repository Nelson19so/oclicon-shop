# 🛍️ Clicon Online Store — Full Stack eCommerce Platform

Clicon is a fully functional eCommerce platform built with a robust Django backend and a responsive, modern frontend using HTML, TailwindCSS, JavaScript, SCSS, and jQuery. It supports both **authenticated and anonymous users** for full CRUD functionality — including cart, wishlist, comparison, checkout, and payment integration using **Paystack**.

---

## 🚀 Features

- 🔐 User Authentication:

  - Register/login with **email or username + password**
  - Google login using **Django AllAuth**
  - Email verification, password reset

- 🛒 Cart & Wishlist (for both authenticated and anonymous users):

  - Add, update, and remove items from cart
  - Add or remove items from wishlist and product comparison

- 📦 Orders & Checkout:

  - Secure checkout flow with **Paystack** integration
  - Payment only creates order after successful verification
  - Order history for logged-in users

- 🛍️ Products:

  - Product listing with search and filtering
  - Product detail pages
  - Admin product management (CRUD)

- 📝 Blog & Ads:

  - Blog post listing and detail views
  - Ad section (banner-style)

- 👤 User Account:

  - View/edit profile picture and details
  - Delete account with data cleanup
  - Track order history

- 💻 UI/UX:

  - Responsive design using TailwindCSS and jQuery
  - SCSS for custom styles
  - AJAX used for dynamic user interactions (cart, wishlist, etc.)

- 🚀 Deployment:
  - Backend hosted on **Render**
  - Static/media files handled with **WhiteNoise**

---

## 🛠️ Tech Stack

| Backend        | Frontend               | Services & Tools          |
| -------------- | ---------------------- | ------------------------- |
| Django         | HTML, CSS, TailwindCSS | PostgreSQL (production)   |
| Django REST    | JavaScript, jQuery     | SQLite (local dev)        |
| Django AllAuth | SCSS, AJAX             | Render (deployment)       |
| Pillow         |                        | WhiteNoise (static files) |

---

## 🔐 Authentication Flow

- Session-based and email/password authentication
- Google login via OAuth using Django AllAuth
- Account activation via email confirmation
- Password reset via email link

---

## 💳 Payment Integration

- Integrated with **Paystack**
- Secure payment flow:
  - Payment page generated with cart total
  - Redirect to Paystack
  - Verified via Paystack API
  - ✅ Order only created **after successful payment**

---

## 📦 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Nelson19so/oclicon-shop.git
cd oclicon-shop
```

2. Set Up Virtual Environment
```bash
bash
Copy
Edit
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```


3. Install Dependencies
```bash
bash
Copy
Edit
pip install -r requirements.txt
```

4. Configure Environment Variables
Create a .env file in the root folder:
```bash
ini
Copy
Edit
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=your_postgres_database_url

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Paystack
PAYSTACK_SECRET_KEY=your_paystack_secret_key
```

5. Apply Migrations
```bash
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
```

6. Run Development Server
```bash
bash
Copy
Edit
python manage.py runserver
```


🌍 Deployment
Hosted backend on Render

Static and media files served via WhiteNoise

Production DB: PostgreSQL on Render

📸 Screenshots
🖼️ Coming soon...

# 👨‍💻 Developer
Name: Nelson Junior
Role: Full Stack Developer (Django, Frontend, Deployment)
Country: Nigeria 🇳🇬
Email: nelsonsomto19@email.com
GitHub: github.com/Nelson19so
LinkedIn: linkedin.com/in/nelson-junior-700b67363

⭐ Contributions & Feedback
Feel free to open issues or pull requests. Feedback is welcome!
