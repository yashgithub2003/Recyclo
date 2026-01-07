# ♻️ Recyclo – E-Waste Management System

> A smart and efficient platform to manage electronic waste collection, recycling, and cost estimation.

Recyclo is a full-stack web application designed to streamline the collection, management, and recycling of electronic waste (e-waste). It connects **customers, collectors, and recyclers** on a single platform and automates the complete e-waste lifecycle — from posting a request to final cost approval.

---

## 🚀 Key Features

### 👤 Customer Module
- Post e-waste pickup requests  
- View cost estimates  
- Approve or reject recycler offers  

### 🚚 Collector Module
- View available pickup requests  
- Accept and complete pickups  
- Deliver e-waste to assigned recyclers  

### 🏭 Recycler Module
- Receive e-waste from collectors  
- Generate reports and estimate recycling value  
- Send price estimates to customers  

### 🛠 Admin Dashboard
- Manage users (Customers, Collectors, Recyclers)  
- Monitor requests, pickups, and deliveries  
- View complete system activity and analytics  

---

## 🛠 Tech Stack

| Layer        | Technology                  |
|-------------|-----------------------------|
| Frontend    | HTML, CSS, JavaScript        |
| Backend     | Python, Django               |
| Database    | SQLite / MySQL               |
| Architecture| Django MVT                   |

---

## 🔄 System Workflow

1. Customer posts an e-waste request  
2. System automatically assigns the **nearest recycler**  
3. Available collector accepts the pickup request  
4. Collector delivers e-waste to recycler  
5. Recycler generates report & cost estimate  
6. Customer approves or rejects the estimate  
7. If approved → process continues  
8. If rejected → product is returned  

---

## ⚙️ Installation & Setup

1️⃣ Clone the Repository
```bash
git clone https://github.com/yashgithub2003/Recyclo.git
cd Recyclo

2️⃣ Create Virtual Environment
python -m venv env
source env/bin/activate   # For Linux/Mac
env\Scripts\activate      # For Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Run the Server
python manage.py runserver

6️⃣ Open in Browser
http://127.0.0.1:8000/
