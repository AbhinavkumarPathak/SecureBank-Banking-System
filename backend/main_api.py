from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("../frontend/index.html")

base_dir = os.path.dirname(os.path.dirname(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")



# Store sessions in memory
sessions = {}

# =========================
# Models
# =========================

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

# =========================
# Helper function
# =========================

def run_bank_command(command):

    bank_path = os.path.join(os.path.dirname(__file__), "bank.exe")

    result = subprocess.run(
        [bank_path] + command[1:],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


# =========================
# Routes
# =========================

@app.get("/", response_class=HTMLResponse)
def read_index():

    base_dir = os.path.dirname(os.path.dirname(__file__))

    file_path = os.path.join(base_dir, "frontend", "index.html")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# REGISTER
@app.post("/register")
def register(data: RegisterRequest):
    output = run_bank_command([
        "bank.exe",
        "create",
        str(data.accNo),
        data.name,
        str(data.pin)
    ])

    if output.startswith("ERROR"):
        raise HTTPException(status_code=400, detail=output)

    return {"status": "success", "message": "Account created successfully"}

# LOGIN
@app.post("/login")
def login(data: LoginRequest):
    output = run_bank_command([
        "bank.exe",
        "balance",
        str(data.accNo),
        str(data.pin)
    ])

    if output.startswith("ERROR"):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = str(uuid.uuid4())
    sessions[token] = {
        "accNo": data.accNo,
        "pin": data.pin
    }

    return {
        "status": "success",
        "token": token,
        "accNo": data.accNo
    }

# BALANCE
@app.post("/balance")
def balance(data: SessionRequest):
    if data.token not in sessions:
        raise HTTPException(status_code=401, detail="Invalid session")

    accNo = sessions[data.token]["accNo"]
    pin = sessions[data.token]["pin"]

    output = run_bank_command([
        "bank.exe",
        "balance",
        str(accNo),
        str(pin)
    ])

    return {
        "status": "success",
        "message": output
    }

# DEPOSIT
@app.post("/deposit")
def deposit(data: TransactionRequest):
    if data.token not in sessions:
        raise HTTPException(status_code=401, detail="Invalid session")

    accNo = sessions[data.token]["accNo"]
    pin = sessions[data.token]["pin"]

    output = run_bank_command([
        "bank.exe",
        "deposit",
        str(accNo),
        str(pin),
        str(data.amount)
    ])

    return {
        "status": "success",
        "message": output
    }

# WITHDRAW
@app.post("/withdraw")
def withdraw(data: TransactionRequest):
    if data.token not in sessions:
        raise HTTPException(status_code=401, detail="Invalid session")

    accNo = sessions[data.token]["accNo"]
    pin = sessions[data.token]["pin"]

    output = run_bank_command([
        "bank.exe",
        "withdraw",
        str(accNo),
        str(pin),
        str(data.amount)
    ])

    return {
        "status": "success",
        "message": output
    }

# HISTORY
@app.post("/history")
def history(data: SessionRequest):
    if data.token not in sessions:
        raise HTTPException(status_code=401, detail="Invalid session")

    accNo = sessions[data.token]["accNo"]
    pin = sessions[data.token]["pin"]

    output = run_bank_command([
        "bank.exe",
        "history",
        str(accNo),
        str(pin)
    ])

    # Parse history output into a list
    history_lines = output.splitlines()
    transactions = []
    for line in history_lines:
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
        "status": "success",
        "transactions": transactions
    }

# LOGOUT
@app.post("/logout")
def logout(data: SessionRequest):
    if data.token in sessions:
        del sessions[data.token]

    return {
        "status": "success",
        "message": "Logged out"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
