# 🛍️ Clicon Online Store — Full Stack eCommerce Platform

Clicon is a fully functional eCommerce platform built with a robust Django backend and a responsive, modern frontend using HTML, TailwindCSS, JavaScript, SCSS, and jQuery. It supports both **authenticated and anonymous users** for full CRUD functionality — including cart, wishlist, comparison, checkout, and payment integration using **Paystack**. Users can also view blogs and it's details + asking questions with customer support

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

- Integrated with (**Paystack**)[https://paystack.com]
- Secure payment flow:
  - Payment page generated with cart total
  - Redirect to (PayStack)[https://paystack.com]
  - Verified via (PayStack)[https://paystack.com] API
  - ✅ Order only created **after successful payment**

---

## Project Structure

```bash

+---apps
ª   +---accounts
ª   ª   +---migrations
ª   ª   ª   +---__pycache__
ª   ª   +---templates
ª   ª   ª   +---accounts
ª   ª   ª       +---authentication
ª   ª   ª       +---forms
ª   ª   +---__pycache__
ª   +---cart
ª   ª   +---migrations
ª   ª   ª   +---__pycache__
ª   ª   +---templates
ª   ª   ª   +---cart
ª   ª   +---__pycache__
ª   +---orders
ª   ª   +---migrations
ª   ª   ª   +---__pycache__
ª   ª   +---templates
ª   ª   ª   +---orders
ª   ª   +---__pycache__
ª   +---payments
ª   ª   +---migrations
ª   ª   ª   +---__pycache__
ª   ª   +---__pycache__
ª   +---products
ª   ª   +---migrations
ª   ª   ª   +---__pycache__
ª   ª   +---templates
ª   ª   ª   +---products
ª   ª   ª       +---partials
ª   ª   +---__pycache__
ª   +---public
ª       +---migrations
ª       ª   +---__pycache__
ª       +---templates
ª       ª   +---public
ª       ª       +---forms
ª       +---__pycache__
+---settings
ª   +---commands
ª   ª   +---__pycache__
ª   +---settings
ª   ª   +---__pycache__
ª   +---__pycache__
+---static
ª   +---images
ª   ª   +---svg
ª   +---js
ª   +---scss
ª   ª   +---abstracts
ª   ª   +---base
ª   ª   +---components
ª   ª   +---layouts
ª   ª   +---pages
ª   ª   +---vendors
ª   +---styles
+---staticfiles
+---templates
    +---email
    +---error
    +---includes
    +---user_accounts

```

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

python manage.py makemigrations accounts
python manage.py makemigrations
```

### **NOTE**: you migrate the accounts app first before any other app

6. Make migrations for all apps

```bash
bash
Copy
Edit

python manage.py makemigrations products
python manage.py makemigrations orders
python manage.py makemigrations cart
python manage.py makemigrations public
python manage.py makemigrations payments

```

- after miking migrations for all apps, then migrate all

```bash
bash
Copy
Edit

python manage.py migrate
```

7. Run Development Server

```bash
bash
Copy
Edit

python manage.py runserver
```

### To make use of the django test

1. Make sure you are on the project root folder

```bash
bash
copy
Edit

cd oclicon-shop
```

2 To test the models run

```bash
bash
copy
Edit

python manage.py test apps.app_name.tests.test_model
```

- **NOTE**: change the '**app_name**' based on the app model you want to test

2 To test the view run

```bash
bash
copy
Edit

python manage.py test apps.app_name.tests.test_view
```

🌍 Deployment
(oclicon-shop)[https://oclicon-shop.onrender.com] backend hosted on (Render)[https://render.com]

Static and media files served via WhiteNoise

Production DB: PostgreSQL on (Render)[https://render.com]

📸 Screenshots
🖼️ Coming soon...

## Observation and what i learned

1. How to auth users with sending email for verification status

2. User profile update, delete verify account

3. Model relation ship (Ont-to-One, Many-to-Many, One-to-Many keys)

- model functions such as @property, save, All etc

4. cart, orders, product, wishlist create, update, read, and delete (CRUD)

5. signals operations

- Implemented for user create account giving user a default profile picture
- Used signals for order history

6. Seeds operations

- Implemented seed operation for creating default categories and children

7. Payment gateway

- implemented a **payment** gateway using PayStack
  - This **payment gateway** is used for paying for orders and also verify reference number

8. Added product ads and banners

9. implemented a newsletter sign-up

10. Django's try and exception for error/null handling

11. How to use **cache** to store items for at least 300s (5 min) to optimize querying

- complete CRUD operation

12. How to use test.py for view and model

**etc...**

---

# 👨‍💻 Developer

- Name: Nelson Junior
- Role: Full Stack Developer (Django, Frontend, Deployment)
- Country: Nigeria 🇳🇬
- Email: nelsonsomto19@email.com
- GitHub: github.com/Nelson19so
- LinkedIn: linkedin.com/in/nelson-junior-700b67363

⭐ Contributions & Feedback
Feel free to open issues or pull requests. Feedback is welcome!
