# Pass_analyzer
Password Strength analyzer and custom wordlist generator

# 🔐 Password Strength Analyzer + Custom Wordlist Generator

A secure and intelligent web tool built with Python and Streamlit that:

- ✅ Analyzes password strength using entropy and validation rules  
- 🧠 Suggests improvements based on 9 industry-standard password rules  
- 📡 Checks for known data breaches using HaveIBeenPwned API  
- 🛠️ Generates a custom wordlist for password testing from personal inputs

---

## 🎯 Features

### 1. Password Strength Analyzer
- Uses `zxcvbn` (by Dropbox) to calculate entropy-based strength
- Visual strength meter with score out of 100%
- Real-time suggestions to improve password security

### 2. Rule-Based Validation (R1–R9)
| Rule | Description |
|------|-------------|
| R1 | Minimum 8 characters required |
| R2 | Must include uppercase letters |
| R3 | Must include lowercase letters |
| R4 | Include at least one digit |
| R5 | Include a special character |
| R6 | Avoid common patterns like `123`, `admin`, `password` |
| R7 | Avoid repeated characters |
| R8 | Avoid sequential characters |
| R9 | Avoid including your name or email in the password |

Each passed rule increases your score.

### 3. Breach Check with HaveIBeenPwned API
- Password hashed (SHA-1) and checked securely
- User gets notified if password appears in any known breaches

### 4. 🧰 Custom Wordlist Generator
- Input base words: name, pet, birth year, etc.
- Generates variations: `name123`, `Name@2025`, `321eman`, `n@me!`
- Downloadable `.txt` file — usable in ethical hacking tools like Hydra, JohnTheRipper

---

## 🚀 How to Run

### 🛠 Install dependencies:

pip install streamlit zxcvbn requests

# ▶️ Launch the app:
streamlit run password_app.py
Then open your browser at: http://localhost:8501

<img width="2880" height="1704" alt="UI" src="https://github.com/user-attachments/assets/0e161c8d-4cdf-4f1b-ac4f-7baf740cda4e" />



# ✅ Benefits
Real-time security feedback

Detects weak or risky passwords

Encourages strong password habits

Wordlist helps in pen-testing or recovery scenarios

Clean, modern web UI (no login required)

# ✨ Future Scope
Add built-in password generator

Export report as PDF/JSON

Deploy to cloud (Streamlit Cloud / Vercel)

Mobile responsive design

Auto email password reports



