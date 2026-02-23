# ================================
# SecureBank Enterprise Backend
# ================================

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import subprocess
import os

# ================================
# JWT SETTINGS
# ================================

SECRET_KEY = "securebank-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# ================================
# CREATE FASTAPI APP
# ================================

app = FastAPI()

# ================================
# PATH SETTINGS
# ================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

BANK_EXE = os.path.join(BASE_DIR, "bank.exe")

# ================================
# MOUNT STATIC FILES
# ================================

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ================================
# TOKEN FUNCTIONS
# ================================

def create_token(accNo, pin):

    payload = {
        "accNo": accNo,
        "pin": pin,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

# ================================
# MODELS
# ================================

class LoginRequest(BaseModel):
    accNo: int
    pin: int


class RegisterRequest(BaseModel):
    accNo: int
    name: str
    pin: int


class SessionRequest(BaseModel):
    token: str


class TransactionRequest(BaseModel):
    token: str
    amount: float


# ================================
# HELPER FUNCTION
# ================================

def run_bank_command(args):

    result = subprocess.run(
        [BANK_EXE] + args,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

# ================================
# SERVE FRONTEND
# ================================

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# ================================
# LOGIN
# ================================

@app.post("/login")
def login(data: LoginRequest):

    output = run_bank_command([
        "balance",
        str(data.accNo),
        str(data.pin)
    ])

    if "ERROR" in output:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_token(data.accNo, data.pin)

    return {
        "status": "success",
        "token": token
    }

# ================================
# REGISTER
# ================================

@app.post("/create")
def create(data: RegisterRequest):

    output = run_bank_command([
        "create",
        str(data.accNo),
        data.name,
        str(data.pin)
    ])

    return {
        "message": output
    }

# ================================
# BALANCE
# ================================

@app.post("/balance")
def balance(data: SessionRequest):

    payload = verify_token(data.token)

    accNo = payload["accNo"]
    pin = payload["pin"]

    output = run_bank_command([
        "balance",
        str(accNo),
        str(pin)
    ])

    return {
        "message": output
    }

# ================================
# DEPOSIT
# ================================

@app.post("/deposit")
def deposit(data: TransactionRequest):

    payload = verify_token(data.token)

    accNo = payload["accNo"]
    pin = payload["pin"]

    output = run_bank_command([
        "deposit",
        str(accNo),
        str(pin),
        str(data.amount)
    ])

    return {
        "message": output
    }

# ================================
# WITHDRAW
# ================================

@app.post("/withdraw")
def withdraw(data: TransactionRequest):

    payload = verify_token(data.token)

    accNo = payload["accNo"]
    pin = payload["pin"]

    output = run_bank_command([
        "withdraw",
        str(accNo),
        str(pin),
        str(data.amount)
    ])

    return {
        "message": output
    }

# ================================
# HISTORY
# ================================

@app.post("/history")
def history(data: SessionRequest):

    payload = verify_token(data.token)

    accNo = payload["accNo"]
    pin = payload["pin"]

    output = run_bank_command([
        "history",
        str(accNo),
        str(pin)
    ])

    transactions = []

    for line in output.splitlines():

        if ":" in line and " at " in line:

            parts = line.split(": ")

            type_part = parts[0]

            amount_time = parts[1].split(" at ")

            transactions.append({
                "type": type_part,
                "amount": amount_time[0],
                "date": amount_time[1]
            })

    return {
        "transactions": transactions
    }

# ================================
# LOGOUT
# ================================

@app.post("/logout")
def logout(data: SessionRequest):

    return {
        "message": "Logged out successfully"
    }

# ================================
# PROFESSIONAL PAGE ROUTES
# ================================

@app.get("/dashboard")
def dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

@app.get("/transfer")
def transfer():
    return FileResponse(os.path.join(FRONTEND_DIR, "transfer.html"))

@app.get("/history-page")
def history_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "history.html"))

@app.get("/profile")
def profile():
    return FileResponse(os.path.join(FRONTEND_DIR, "profile.html"))

@app.get("/settings")
def settings():
    return FileResponse(os.path.join(FRONTEND_DIR, "settings.html"))