# Django Online Shop **TB_TG**

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)
![Static Badge](https://img.shields.io/badge/TestCoverage-90%20%25-red)
![Static Badge](https://img.shields.io/badge/Django-v5.0.1-lightgreen)
![Static Badge](https://img.shields.io/badge/Python-v3.11.7-blue)

A full-stack online shop built with Django, JavaScript, HTML, and CSS.

## Features

- **User Authentication<span style="color:lime;"> (JWT)</span>**: Allow users to sign up, log in, and log out using JSON
  Web Tokens (JWT) for secure authentication.


- **Product Dynamic Filtering**: Display a list of products with details and provide dynamic filtering options to help
  users find products based on various criteria such as category, price range, etc.


- **Shopping Cart**: Enable users to add products to a shopping cart, update quantities, and remove items, providing a
  seamless shopping experience.


- **Checkout with<span style="color:cyan;"> Zarinpal</span>**: Allow users to proceed to checkout, enter shipping and
  payment details, and securely process payments using Zarinpal payment gateway.


- **Blog and Comments**: Implement a blog feature where users can read articles and leave comments, fostering community
  engagement and interaction.


- **Admin Panel**: Provide administrators with a comprehensive admin dashboard to manage products, orders, users, and
  other site content efficiently.


- **Audit Log**: Keep track of important actions and changes made within the system, providing transparency and
  accountability.


- **Product Reviews**: Allow users to leave reviews and ratings for products, helping other users make informed
  purchasing decisions.


- **Translation**: Implement multi-language support to ensure the website is accessible to users from different
  linguistic backgrounds, enhancing user experience and inclusivity.


- **Dynamic SiteSettings (Django Solo)**: Enables easy site customization for administrators with multi-language support
  for accessibility.


- **Performance Testing with Silk and Locust**: Utilize Silk and Locust for comprehensive performance testing to assess
  system behavior under varying loads, ensuring application scalability and reliability.


- **Test Coverage 90%**: Aim for <span style="color:red;">90% test coverage</span>  using pytest and coverage to improve
  code quality and reliability.


- **Self-Relational Category System**: Organize products hierarchically, simplifying navigation and management for users
  and admins, enhancing shop scalability and organization.


- **Caching with Django-Compressor and Redis**: Optimize performance using Django-Compressor for CSS and JavaScript
  caching, and Redis cache for efficient view caching.


- **API Documentation with Swagger**: Utilize Swagger for API documentation by configuring an endpoint with `/schema_view/`
  to render Swagger UI, enhancing API usability and accessibility.



- **Celery Tasks & Flower Monitoring**:

-- **delete_inactive_users**: Deletes inactive users after three days.
-- **send_promotion_emails**: Sends recent promotions via email.
-- **send_birthday_emails**: Sends birthday greetings via email.
-- **delete_old_carts**: Deletes old carts after five days.
Flower is used for Celery monitoring.


- **<span style="color:orange;">Selenium</span> Test Features**: Add Selenium tests for each feature to ensure functionality and user experience across the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/django-online-shop.git
   cd django-online-shop

2. Install dependencies:
   ```python
   pip install -r requirements.txt

3. Apply migrations:
   ```python
   python manage.py migrate

4. Create a superuser:
   ```python
   python manage.py createsuperuser

5. Run the development server:
   ```python
   python manage.py runserver

6. Access the application at http://localhost:8000.
