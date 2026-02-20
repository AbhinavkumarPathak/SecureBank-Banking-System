// LIVE BACKEND URL
const API_BASE = "https://securebank-pq4s.onrender.com";

let token = "";
let currentUser = "";

// SWITCH VIEW
function showView(viewId) {

    document.getElementById("loginView").style.display = "none";
    document.getElementById("registerView").style.display = "none";
    document.getElementById("dashboardView").style.display = "none";

    document.getElementById(viewId).style.display = "block";
}


// LOGIN
async function handleLogin() {

    const accNo = document.getElementById("accNo").value;
    const pin = document.getElementById("pin").value;

    if (!accNo || !pin) {
        document.getElementById("loginStatus").innerText = "Enter credentials";
        return;
    }

    try {

        const res = await fetch(API_BASE + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                accNo: parseInt(accNo),
                pin: parseInt(pin)
            })
        });

        const data = await res.json();

        if (res.ok) {

            token = data.token;
            currentUser = accNo;

            document.getElementById("userNameDisplay").innerText =
                "Welcome, Account " + accNo;

            showView("dashboardView");

            await updateBalance();
            await loadHistory();

        } else {

            document.getElementById("loginStatus").innerText =
                data.detail || "Login failed";

        }

    } catch (error) {

        document.getElementById("loginStatus").innerText = "Server error";
        console.error(error);

    }
}


// REGISTER
async function handleRegister() {

    const accNo = document.getElementById("regAccNo").value;
    const name = document.getElementById("regName").value;
    const pin = document.getElementById("regPin").value;

    if (!accNo || !name || !pin) {

        document.getElementById("regStatus").innerText = "Fill all fields";
        return;
    }

    try {

        const res = await fetch(API_BASE + "/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                accNo: parseInt(accNo),
                name: name,
                pin: parseInt(pin)
            })
        });

        const data = await res.json();

        document.getElementById("regStatus").innerText =
            data.message || "Account created";

    } catch {

        document.getElementById("regStatus").innerText =
            "Registration failed";

    }
}


// BALANCE
async function updateBalance() {

    try {

        const res = await fetch(API_BASE + "/balance", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                token: token
            })
        });

        const data = await res.json();

        document.getElementById("balanceDisplay").innerText =
            data.message || "Balance unavailable";

    } catch {

        document.getElementById("balanceDisplay").innerText =
            "Error loading balance";

    }
}


// TRANSACTION (FIXED)
async function handleTransaction(type) {

    const amount = document.getElementById("amount").value;

    if (!amount) return;

    try {

        const res = await fetch(API_BASE + "/" + type, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                token: token,
                amount: parseFloat(amount)
            })

        });

        const data = await res.json();

        document.getElementById("dashStatus").innerText =
            data.message || "Transaction complete";

        await updateBalance();
        await loadHistory();

    } catch {

        document.getElementById("dashStatus").innerText =
            "Transaction failed";

    }
}


// LOGOUT
async function handleLogout() {

    await fetch(API_BASE + "/logout", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            token: token
        })

    });

    token = "";
    currentUser = "";

    showView("loginView");
}


// HISTORY
async function loadHistory() {

    try {

        const res = await fetch(API_BASE + "/history", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                token: token
            })

        });

        const data = await res.json();

        const list = document.getElementById("transactionList");

        list.innerHTML = "";

        if (!data.transactions || data.transactions.length === 0) {

            list.innerHTML =
                '<div class="empty-state">No transactions yet</div>';
            return;
        }

        data.transactions.forEach(tx => {

            let icon = "fa-circle";
            let color = "#ccc";

            if (tx.type.toLowerCase().includes("deposit")) {
                icon = "fa-arrow-down";
                color = "#00ffa3";
            }

            if (tx.type.toLowerCase().includes("withdraw")) {
                icon = "fa-arrow-up";
                color = "#ff6b6b";
            }

            const item = document.createElement("div");

            item.className = "transaction-item";

            item.innerHTML = `
                <div style="display:flex;justify-content:space-between;width:100%">
                    <div>
                        <i class="fas ${icon}" style="color:${color}"></i>
                        ${tx.type}
                    </div>
                    <div>
                        ₹${tx.amount}
                    </div>
                    <div style="opacity:0.6;font-size:12px">
                        ${tx.date}
                    </div>
                </div>
            `;

            list.appendChild(item);

        });

    } catch (error) {

        console.error("History load failed:", error);

    }
}