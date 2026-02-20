# 🏦 SecureBank – Banking Management System

SecureBank is a full-stack banking management system built using a high-performance C++ backend engine, FastAPI REST API, SQLite database, and a modern responsive frontend. It simulates real-world banking operations including authentication, deposits, withdrawals, balance tracking, and transaction history with timestamps.

This project demonstrates system design, backend integration, database management, and API development suitable for production-level applications.

---

## 🚀 Features

### 🔐 Authentication
- Secure login using Account Number and PIN
- Session-based authentication using tokens
- Protected API endpoints

### 💰 Account Operations
- Create new bank account
- Deposit money
- Withdraw money
- Check real-time balance

### 📜 Transaction Management
- Automatic transaction recording
- Timestamped transactions
- Transaction history with proper formatting
- Latest transactions displayed first

### 🌐 Full Stack Integration
- C++ core banking engine
- FastAPI backend API
- SQLite persistent database
- Modern responsive frontend (HTML, CSS, JavaScript)

---

## 🏗️ Architecture

Frontend (HTML/CSS/JS)
│
▼
FastAPI Backend (Python)
│
▼
C++ Banking Engine (bank.exe)
│
▼
SQLite Database (bank.db)


---

## 🛠️ Technologies Used

| Layer | Technology |
|------|------------|
| Core Engine | C++ |
| Backend API | FastAPI (Python) |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| API Communication | REST API |
| Authentication | Session Tokens |
| Build Tools | gcc, g++ |
| Server | Uvicorn |

---

## 📂 Project Structure

SecureBank/
│
├── backend/
│ ├── main_api.py # FastAPI backend
│ ├── main.cpp # C++ banking engine
│ ├── bank.exe # Compiled C++ executable
│ ├── sqlite3.c
│ ├── sqlite3.h
│ └── bank.db # SQLite database
│
├── frontend/
│ └── index.html # UI
│
├── static/
│ ├── style.css
│ └── script.js
│
├── requirements.txt
└── README.md


---

⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/SecureBank.git
cd SecureBank

Install Python dependencies
pip install -r requirements.txt

3. Compile C++ engine

Navigate to backend folder:

cd backend


Compile SQLite:

gcc -c sqlite3.c -o sqlite3.o


Compile main program:

g++ main.cpp sqlite3.o -o bank.exe

4. Run FastAPI server
python -m uvicorn main_api:app --reload


Server will start at:

http://127.0.0.1:8000

5. Open in browser
http://127.0.0.1:8000

📸 Application Preview

Features demonstrated:

Login system

Balance dashboard

Deposit & withdraw

Transaction history

Real-time database updates

🧪 Example Commands (C++ Engine)
bank.exe create 1001 Abhinav 1234
bank.exe deposit 1001 1234 500
bank.exe withdraw 1001 1234 200
bank.exe balance 1001 1234
bank.exe history 1001 1234

🔒 Security Features

Token-based session authentication

Credential verification

Protected transaction endpoints

Database integrity enforcement

🎯 Learning Outcomes

This project demonstrates:

Backend system design

REST API development

Database integration

C++ and Python interoperability

Authentication implementation

Full-stack application architecture

📈 Future Improvements

Online deployment (AWS / Render / Railway)

Admin dashboard

Money transfer between accounts

JWT authentication

Docker containerization

👨‍💻 Author

Abhinav Kumar Pathak
B.Tech Computer Science Engineering
Cloud Computing Major | Android Development Minor

⭐ Why this project is valuable

This project demonstrates real-world backend engineering skills including:

System architecture

API development

Database design

C++ and Python integration

Secure authentication

Suitable for backend developer, software engineer, and system engineer roles.

📜 License

This project is for educational and demonstration purposes.

