<h1 align="center"><u> 📌Find information by phone number 😮 </u></h1>

⚠️ Use for educational purposes only

---

# 📞 PhoneXtract - Number Intelligence Tool

PhoneXtract is a simple yet powerful OSINT-based tool built in Python for gathering basic information about any phone number (Indian numbers preferred). Ideal for educational purposes and security researchers.

> 🔧 Created by: **Alok Thakur**
> 📺 YouTube: **Firewall Breaker**

---

## ⚙️ Features

- 📍 Get the location (state-level) of the phone number
- 📡 Detect carrier name (Airtel, Jio, etc.)
- 📞 Identify phone type (Mobile, Landline, VoIP)
- 🕰️ Time zone of the number
- 🌐 National & International formats
- ✅ Validity check of the number
- 🔠 Prefix and area code analysis
- 🏙️ City/State (approximate via prefix mapping)
- 🚫 Placeholder sections for:
  - Spam reports
  - Risk score
  - Data breach info

---

## 🌐 International Number Support

> **Note:** PhoneXtract works with global numbers using the `phonenumbers` library, but:
> - City/state detection is only optimized for Indian numbers.
> - International numbers will show only basic info like country, timezone, and type.
> - Prefix-based lookup is India-specific.

---

## 📲 Termux Installation (Android)

```bash
pkg update && pkg upgrade -y
```

```bash
pkg install git -y
```

```bash
git clone https://github.com/thakur2309/phonextract.git
```

```bash
cd phonextract
```

```bash
pip install -r requirements.txt
```

### ▶️ Start Command

```bash
python3 phonextract.py
```

### 📦 One-Line Install (Termux)

```bash
pkg update && pkg upgrade && pkg install git && git clone https://github.com/thakur2309/phonextract.git && cd phonextract && pip install -r requirements.txt && python3 phonextract.py
```

---

## 🐉 Kali Linux Installation (Using venv)

> Kali Linux me system-wide pip install blocked hoti hai, isliye **virtual environment (venv)** use karna recommended hai.

### Step 1 — System Update karo

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2 — Python venv support install karo

```bash
sudo apt install python3-venv python3-pip git -y
```

### Step 3 — Repository Clone karo

```bash
git clone https://github.com/thakur2309/phonextract.git
```

### Step 4 — Folder me jao

```bash
cd phonextract
```

### Step 5 — Virtual Environment banao

```bash
python3 -m venv venv
```

### Step 6 — venv Activate karo

```bash
source venv/bin/activate
```

> ✅ Ab terminal ke aage `(venv)` dikhega — matlab venv active hai.

### Step 7 — Dependencies install karo

```bash
pip install -r requirements.txt
```

### Step 8 — Tool chalao

```bash
python3 phonextract.py
```

---

### ⚡ Kali Linux — One-Line Install (venv ke saath)

```bash
sudo apt update && sudo apt install python3-venv python3-pip git -y && git clone https://github.com/thakur2309/phonextract.git && cd phonextract && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 phonextract.py
```

---

### 🔁 Dobara Use Karne ke Liye (Kali Linux)

Jab bhi tool dobara use karna ho, ye commands chalao:

```bash
cd phonextract
source venv/bin/activate
python3 phonextract.py
```

---

### ❌ venv Deactivate Karna

```bash
deactivate
```

---

## 📌 Contact Me

<a href="https://youtube.com/@firewallbreaker09">
  <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube">
</a>
<br>
<a href="https://github.com/thakur2309?tab=repositories">
  <img src="https://img.shields.io/badge/GitHub-000000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
<br>
<a href="https://whatsapp.com/channel/0029VbAiqVMKLaHjg5J1Nm2F">
  <img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp Channel">
</a>
