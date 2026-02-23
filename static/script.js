// ===============================
// SecureBank Enterprise Script
// ===============================

// Backend API
const API = "https://securebank-pq4s.onrender.com";

// Session variables
let token = localStorage.getItem("token") || "";
let currentUser = localStorage.getItem("currentUser") || "";


// ===============================
// AUTO LOGIN IF TOKEN EXISTS
// ===============================

window.onload = function () {

    if (token) {

        showView("dashboardView");

        document.getElementById("userNameDisplay").innerText =
            "Welcome, Account " + currentUser;

        updateBalance();
        loadHistory();
    }
};


// ===============================
// SWITCH VIEW
// ===============================

function showView(viewId) {

    const views = ["loginView", "registerView", "dashboardView"];

    views.forEach(v => {
        const el = document.getElementById(v);
        if (el) el.style.display = "none";
    });

    const target = document.getElementById(viewId);
    if (target) target.style.display = "block";
}


// ===============================
// LOGIN
// ===============================

async function handleLogin() {

    const accNo = document.getElementById("accNo").value;
    const pin = document.getElementById("pin").value;

    if (!accNo || !pin) {

        document.getElementById("loginStatus").innerText =
            "Enter credentials";

        return;
    }

    try {

        const res = await fetch(API + "/login", {

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

            // Save session
            localStorage.setItem("token", token);
            localStorage.setItem("currentUser", currentUser);

            document.getElementById("userNameDisplay").innerText =
                "Welcome, Account " + accNo;

            showView("dashboardView");

            await updateBalance();
            await loadHistory();

        }
        else {

            document.getElementById("loginStatus").innerText =
                data.detail || "Login failed";
        }

    }
    catch (error) {

        document.getElementById("loginStatus").innerText =
            "Server error";
    }
}


// ===============================
// REGISTER
// ===============================

async function handleRegister() {

    const accNo = document.getElementById("regAccNo").value;
    const name = document.getElementById("regName").value;
    const pin = document.getElementById("regPin").value;

    if (!accNo || !name || !pin) {

        document.getElementById("regStatus").innerText =
            "Fill all fields";

        return;
    }

    try {

        const res = await fetch(API + "/create", {

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

    }
    catch {

        document.getElementById("regStatus").innerText =
            "Registration failed";
    }
}


// ===============================
// BALANCE
// ===============================

async function updateBalance() {

    if (!token) return;

    try {

        const res = await fetch(API + "/balance", {

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

    }
    catch {

        document.getElementById("balanceDisplay").innerText =
            "Error";
    }
}


// ===============================
// TRANSACTION
// ===============================

async function handleTransaction(type) {

    const amount = document.getElementById("amount").value;

    if (!amount || !token) return;

    try {

        const res = await fetch(API + "/" + type, {

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
            data.message || "Success";

        await updateBalance();
        await loadHistory();

    }
    catch {

        document.getElementById("dashStatus").innerText =
            "Transaction failed";
    }
}


// ===============================
// LOGOUT
// ===============================

async function handleLogout() {

    try {

        await fetch(API + "/logout", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                token: token
            })

        });

    } catch {}

    token = "";
    currentUser = "";

    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");

    showView("loginView");
}


// ===============================
// HISTORY
// ===============================

async function loadHistory() {

    if (!token) return;

    try {

        const res = await fetch(API + "/history", {

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
                    <div>₹${tx.amount}</div>
                    <div style="opacity:0.6;font-size:12px">${tx.date}</div>
                </div>
            `;

            list.appendChild(item);
        });

    }
    catch {

        document.getElementById("transactionList").innerHTML =
            '<div class="empty-state">Failed to load transactions</div>';
    }
}