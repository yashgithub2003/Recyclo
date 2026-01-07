♻️ Recyclo – E-Waste Management System

Recyclo is a full-stack web application designed to streamline the collection, management, and recycling of electronic waste (e-waste). The system connects customers, collectors, and recyclers on a single platform and automates the complete e-waste lifecycle from posting a request to final cost approval.

🚀 Features

Customer Module

Post e-waste pickup requests

View cost estimates and approve/reject offers

Collector Module

View available pickup requests

Accept and complete pickups

Deliver e-waste to assigned recyclers

Recycler Module

Receive e-waste from collectors

Generate reports and estimate recycling value

Send price estimates to customers

Admin Dashboard

Manage users (customers, collectors, recyclers)

Monitor requests, pickups, and system activity

View overall platform analytics

🛠 Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Python, Django

Database: SQLite (default) / MySQL

Framework: Django (MVT Architecture)

🔄 Workflow

Customer posts an e-waste request

System automatically assigns the nearest recycler

Available collector accepts the pickup request

Collector delivers e-waste to recycler

Recycler generates report and cost estimate

Customer approves or rejects the estimate

If approved → process continues, if rejected → product is returned

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/yashgithub2003/Recyclo.git
cd recyclo


Create virtual environment

python -m venv env
source env/bin/activate   # For Linux/Mac
env\Scripts\activate      # For Windows


Install dependencies

pip install -r requirements.txt


Apply migrations

python manage.py makemigrations
python manage.py migrate


Run the server

python manage.py runserver


Open in browser:

http://127.0.0.1:8000/
