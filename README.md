---

# 🛍️ Clicon Online Store — eCommerce Project

A fully functional eCommerce platform built using **Django** for the backend and **HTML, CSS, TailwindCSS, JavaScript, and jQuery** for the frontend.

---

## 🚀 Features

- User registration and login (email/username/password + Google OAuth)
- email confirmation, reset password
- Product listing + filtering and detail pages
- Add to cart, update quantity, remove from cart
- Add to wishlist, Compare and Remove 
- Checkout and order processing/order tracking
- User profile with order history
- Admin product management (CRUD)
- blog post listing and details
- ads and so on
- Responsive UI using TailwindCSS and jQuery + scss
- Deployed backend on **Render**

---

## 🛠️ Tech Stack

| Backend        | Frontend             | Other Services            |
|----------------|----------------------|----------------------------|
| Django         | HTML, CSS, Tailwind  | Django AllAuth (Google)   |
| Django AllAuth | JavaScript, jQuery   | PostgreSQL                |
| Pillow         | SCSS (optional)      | Render (deployment)       |

---

## 🔐 Authentication

- Users can register using **email or username + password**
- Google login via **Django AllAuth**
- JWT or session-based login supported

---

## 📦 How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/clickon-ecommerce.git
cd clickon-ecommerce

2. Set up virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Environment variables

Create a .env file with:

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=your_postgres_url
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_secret

5. Run migrations

python manage.py makemigrations
python manage.py migrate

6. Run server

python manage.py runserver


---

🌐 Deployment

Backend is deployed on Render.
Static files served using WhiteNoise.


---

📸 Screenshots

loading...


---

👨‍💻 Developer

Name: Nelson

Role: Backend Developer (Django) + Front-end developer 

Country: Nigeria 🇳🇬

Email: nelsonsomto19@email.com

LinkedIn: https://www.linkedin.com/in/nelson-junior-700b67363?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app

GitHub: github.com/Nelson19so 
