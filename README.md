# oclicon-shop

Created and ecommerce web app using html, css, scss, Tailwindcss, javascript, jquery and django &amp; PosgresSQL. this webapp is an online store where users can be able to buy electronics online and access their profile/dashboard. this gave me a deep understanding on how to handle large dataset and manage extensive code.

## libraris to install to run django

- Django
- django-crispy-forms
- crispy-bootstrap5
- Pillow
- django-allauth
- django-oauth-toolkit
- django-widget-tweaks
- django-debug-toolbar
- whitenoise
- psycopg2-binary
- dj-database-url
- gunicorn

  <------------------------------------>

# djang

- django-widget-tweaks is a Django package that allows you to customize form field widgets dynamically in templates.

eg: "
{% load widget_tweaks %}

<!-- <form method="POST">
    {% csrf_token %}

    <!-- Add Bootstrap classes dynamically -->

    <div class="form-group">
        {{ form.username|add_class:"form-control" }}
    </div>

    <div class="form-group">
        {{ form.password|add_class:"form-control is-invalid" }}
    </div>

    <button type="submit" class="btn btn-primary">Login</button>

</form> -->

"

- django-widget-tweaks is a Django package that allows you to customize form field widgets dynamically in templates.

- dj-database-url is a Django package that helps configure your database settings using a single environment variable. It's especially useful for deployment (e.g., on Heroku, Render, or Docker) where database URLs are provided dynamically.

## to generate folder structure to look at

- tree /F /A > structure.txt
