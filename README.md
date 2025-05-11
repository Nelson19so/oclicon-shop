Oclicon Online Store

Clicon Online Store is a fully-featured eCommerce web application built with Django for the backend and enhanced with a modern, responsive frontend using HTML, CSS, SCSS, TailwindCSS, JavaScript, and jQuery. The project includes user authentication, product management, cart functionality, an admin dashboard, order processing, and much more.

This project is designed to showcase my skills as a backend developer, but it also integrates frontend technologies for a complete shopping experience. It can serve as a template for building scalable, production-ready eCommerce platforms.

Features

User Authentication: Custom user model, sign-up, login,email verification, password reset code,password reset,Google, and Apple login integration (via Django AllAuth).

Product Management: Ability to add, update, delete, and display products dynamically.

Cart System: Add, update, and remove products in the shopping cart.

Order Management: Users can place orders, view order details, and track order status.

Wishlist: Users can save products to their wishlist.

Admin Dashboard: A simple, secure dashboard to manage orders, products, and users.

Responsive UI: Fully responsive and mobile-friendly interface with clean UI/UX.

AJAX: Implemented AJAX to enhance the user experience for real-time interactions (such as updating the cart).

Security: Secure user authentication, password hashing, and protection against CSRF/XSS.


Tech Stack

Frontend:

HTML5, CSS3, SCSS, Tailwind CSS

JavaScript, jQuery

AJAX (for dynamic content updates)


Backend:

Django (for the API and server-side logic)

Django Rest Framework (for API-based functionalities)

PostgreSQL (database)

Pillow (for image handling)

Django AllAuth (for Google and Apple authentication)



Setup and Installation

1. Clone the Repository:

git clone https://github.com/yourusername/clickon.git


2. Set up a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


3. Install Dependencies:

pip install -r requirements.txt


4. Set Up Database: Make sure PostgreSQL is installed and running. Create a database for the project.

python manage.py migrate


5. Run the Development Server:

python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser to see the application.


6. Optional - Create Superuser for Admin Panel:

python manage.py createsuperuser



Environment Variables

Ensure you have the following environment variables set up in a .env file (or use django-environ for better management):

DATABASE_URL (PostgreSQL connection string)

SECRET_KEY (Django secret key)

DEBUG (True or False)

ALLOWED_HOSTS (list of allowed hosts)

GOOGLE_CLIENT_ID (for Google Authentication)

APPLE_CLIENT_ID (for Apple Authentication)


Future Improvements

Payment Gateway Integration: Integrate payment options like Stripe or PayPal for order payments.

Ratings & Reviews: Allow users to leave product reviews and rate them.

Product Search: Implement search functionality with filters (by category, price, etc.).

Product Recommendations: Add a recommendation system based on user activity.


Screenshots

(Include some screenshots of your project in action, such as the homepage, product page, cart, admin dashboard, etc.)

Contribution

Feel free to fork this repository and contribute by submitting issues, pull requests, or feature suggestions.
