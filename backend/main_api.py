from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
import bcrypt

# JWT imports
from jose import jwt
from datetime import datetime, timedelta


# JWT settings
SECRET_KEY = "securebank-secret-key"
ALGORITHM = "HS256"


# Create FastAPI app
app = FastAPI()


# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
BANK_EXE = os.path.join(BASE_DIR, "bank.exe")


# Mount static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# Serve frontend
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# Models
class LoginRequest(BaseModel):
    accNo: int
    pin: int


class RegisterRequest(BaseModel):
    accNo: int
    name: str
    pin: int


class TokenRequest(BaseModel):
    token: str


class TransactionRequest(BaseModel):
    token: str
    amount: float


# Helper to run bank.exe
def run_bank_command(args):

    result = subprocess.run(
        [BANK_EXE] + args,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


# JWT verify function
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


# LOGIN
@app.post("/login")
def login(data: LoginRequest):

    # check using bank.exe
    output = run_bank_command([
        "balance",
        str(data.accNo),
        str(data.pin)
    ])

    if "ERROR" in output:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "accNo": data.accNo,
        "pin": data.pin,
        "exp": datetime.utcnow() + timedelta(hours=5)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "status": "success",
        "token": token
    }


# REGISTER
@app.post("/create")
def create(data: RegisterRequest):

    # hash PIN
    hashed_pin = bcrypt.hashpw(
        str(data.pin).encode(),
        bcrypt.gensalt()
    ).decode()

    output = run_bank_command([
        "create",
        str(data.accNo),
        data.name,
        hashed_pin
    ])

    return {
        "message": output
    }


# BALANCE
@app.post("/balance")
def balance(data: TokenRequest):

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


# DEPOSIT
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


# WITHDRAW
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


# HISTORY
@app.post("/history")
def history(data: TokenRequest):

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


# LOGOUT
@app.post("/logout")
def logout(data: TokenRequest):

    # JWT logout handled client-side
    return {
        "message": "Logged out"
    }
    
    
from fastapi.responses import FileResponse

@app.get("/dashboard")
def dashboard():
    return FileResponse("templates/dashboard.html")

@app.get("/transfer")
def transfer():
    return FileResponse("templates/transfer.html")

@app.get("/history-page")
def history_page():
    return FileResponse("templates/history.html")

@app.get("/profile")
def profile():
    return FileResponse("templates/profile.html")

@app.get("/settings")
def settings():
    return FileResponse("templates/settings.html")