Oclicon Online Store

Clicon Online Store is a fully-featured eCommerce web application built with Django for the backend and enhanced with a modern, responsive frontend using HTML, CSS, SCSS, TailwindCSS, JavaScript, and jQuery. It includes user authentication, product management, cart functionality, an admin dashboard, order processing, wishlist, and more.

This project showcases my backend development skills while also featuring a complete frontend experience. It can serve as a robust template for scalable, production-ready eCommerce platforms.

---

Features

User Authentication:
Custom user model, sign-up, login, email verification, password reset code & form, Google and Apple login (via Django AllAuth).

Product Management:
Add, update, delete, and display products dynamically.

Cart System:
Add, update, and remove items in the shopping cart.

Order Management:
Place orders, view order details, and track order status.

Wishlist:
Save products to a wishlist for future reference.

Admin Dashboard:
Secure admin interface for managing orders, users, and inventory.

Responsive UI:
Fully mobile-friendly and responsive layout.

AJAX:
Enhances user experience with real-time updates (like cart actions).

Security:
Password hashing, CSRF/XSS protection, and secure authentication.

---

Tech Stack

Frontend

HTML5, CSS3, SCSS, Tailwind CSS

JavaScript, jQuery

AJAX for dynamic interaction

Backend

Django

Django REST Framework

PostgreSQL

Pillow (image handling)

Django AllAuth (OAuth with Google and Apple)

---

Setup & Installation

1. Clone the Repository

git clone https://github.com/yourusername/clickon.git
cd clickon

2. Set up a Virtual Environment

python -m venv venv

# On Windows

venv\Scripts\activate

# On macOS/Linux

source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure PostgreSQL Database

Ensure PostgreSQL is installed and running. Then set up your database and update your .env or settings.py accordingly.

python manage.py migrate

5. Create Superuser (Optional)

python manage.py createsuperuser

6. Run the Server

python manage.py runserver

Visit: http://127.0.0.1:8000/

---

Environment Variables

Create a .env file and add the following:

DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GOOGLE_CLIENT_ID=your_google_client_id
APPLE_CLIENT_ID=your_apple_client_id

---

Future Improvements

Payment Gateway Integration – Stripe or PayPal

Product Ratings & Reviews

Advanced Search and Filters

Recommendation System

---

Screenshots

loading...

---

Contribution

Feel free to fork this repository and open pull requests or issues. Suggestions and improvements are welcome.
