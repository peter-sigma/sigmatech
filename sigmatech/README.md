# Sigmatech Online Ordering System

Sigmatech Online Ordering System is a web-based eCommerce platform designed for selling electronics. It allows users to browse products, place orders, and make payments online. The system includes features such as real-time order updates, product management, and secure payment processing via PayPal.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Features](#features)
7. [Project Structure](#project-structure)
8. [API Reference](#api-reference)
9. [Contributing](#contributing)
10. [License](#license)

---

## Project Overview

Sigmatech is designed to simplify the sale and purchase of electronic products. It provides an easy-to-use interface for customers to browse electronics, add items to their shopping cart, and complete purchases securely via PayPal.

---

## Technologies Used
- **Backend**: Django (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Real-Time Features**: Django Channels
- **Payment Gateway**: PayPal API
- **Version Control**: Git

---

## Installation Guide

### Pre-requisites
Before running the project, ensure you have the following installed:
- Python 3.8+
- Git
- Virtualenv (optional but recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/peter-sigma/sigmatech.git
cd sigmatech


## Step 2: 
Create and Activate a Virtual Environment
bash
Copy code
### Create a virtual environment
python -m venv env

### Activate the virtual environment
#### On Windows
env\Scripts\activate

#### On macOS/Linux
source env/bin/activate
### Step 3: Install Dependencies
bash
Copy code
pip install -r requirements.txt
Step 4: Set Up the Database
Run the following command to create the SQLite database and apply migrations:

bash
Copy code
python manage.py migrate
Step 5: Create a Superuser
To access the admin dashboard, create a superuser account:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to set a username, email, and password.

Step 6: Run the Development Server
bash
Copy code
python manage.py runserver
Access the project in your web browser at http://127.0.0.1:8000/.

## Configuration
### Database Settings
The project is configured to use SQLite by default. If you wish to use another database (e.g., PostgreSQL), modify the DATABASES setting in settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

### PayPal Settings
Add your PayPal credentials to the settings.py file:

PAYPAL_CLIENT_ID = 'your-paypal-client-id'
PAYPAL_CLIENT_SECRET = 'your-paypal-client-secret'

## SMTP Configuration (for Email Notifications)

Configure SMTP settings to send order confirmations:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'


## Usage

### Admin Dashboard
The admin dashboard allows you to manage products, orders, and users. You can add, edit, and delete products, as well as view and manage orders. 
To manage products, orders, and users, access the Django admin at:
http://127.0.0.1:8000/sigmatech/admin

### Product Browsing
The product browsing page allows users to view all available products. Users can filter products by category, brand, or price.
Users can browse through the product catalog and view categories at the main site:
http://127.0.0.1:8000/product/catalog/
You can also click on the links in the navigation bar named windowshop

### Shopping and payment
Add products to the shopping cart.
Proceed to checkout, where users can make payments via PayPal.
Features
Product Catalog: Browse and search electronics.
Shopping Cart: Add and remove items from the cart.
Checkout: Secure payment via PayPal.
Real-Time Updates: Order status updates using Django Channels.
Admin Dashboard: Manage products, categories, and orders.

### Project Structure
sigmatech-online-ordering-system/
│
├── cart/               # Handles the shopping cart functionality
├── core/               # Core settings and utilities
├── dashboard/          # Admin views and dashboard management
├── order/              # Order processing and management
├── payment/            # Payment integration (PayPal)
├── product/            # Product and category models and views
├── user/               # User authentication and profile management
│
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
│
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies




