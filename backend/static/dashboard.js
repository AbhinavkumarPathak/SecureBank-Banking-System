const API="https://securebank-pq4s.onrender.com";

let token=localStorage.getItem("token");

async function loadBalance(){

const res=await fetch(API+"/balance",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({token})
});

const data=await res.json();

document.getElementById("balance").innerText=data.message;
}

async function deposit(){

let amount=document.getElementById("depositAmount").value;

await fetch(API+"/deposit",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({token,amount})
});

loadBalance();
loadHistory();
}

async function withdraw(){

let amount=document.getElementById("withdrawAmount").value;

await fetch(API+"/withdraw",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({token,amount})
});

loadBalance();
loadHistory();
}

async function loadHistory(){

const res=await fetch(API+"/history",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({token})
});

const data=await res.json();

const div=document.getElementById("transactions");

div.innerHTML="";

data.transactions.forEach(tx=>{

div.innerHTML+=`
<div>
${tx.type} ₹${tx.amount} ${tx.date}
</div>
`;

});

}

loadBalance();
loadHistory();