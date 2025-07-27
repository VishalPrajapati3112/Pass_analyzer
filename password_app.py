# password_app.py

import streamlit as st
import re, hashlib, requests
from zxcvbn import zxcvbn
import io

# -------- Password Rules (R1–R9) --------
def validate_password(password, username=None):
    issues = []

    if len(password) < 8:
        issues.append("R1: Too short (min 8 characters)")
    if not re.search(r"[A-Z]", password):
        issues.append("R2: Add at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        issues.append("R3: Add at least one lowercase letter")
    if not re.search(r"[0-9]", password):
        issues.append("R4: Include at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("R5: Use special characters (@#$%^&*)")
    if any(p in password.lower() for p in ['123', 'abc', 'qwerty', 'password', 'admin']):
        issues.append("R6: Avoid common patterns like '123', 'qwerty', 'admin'")
    if re.search(r'(.)\1{2,}', password):
        issues.append("R7: Avoid repeating characters like 'aaa' or '111'")
    if re.search(r'(0123|1234|2345|abcd|bcde|qwerty|asdf)', password.lower()):
        issues.append("R8: Avoid sequential characters like '1234' or 'abcd'")
    if username and username.lower() in password.lower():
        issues.append("R9: Don’t include your name, email or username in the password")

    return issues

def count_passed_rules(password, username=None):
    total = 9
    failed = len(validate_password(password, username))
    return total - failed

# -------- Breach Check --------
def check_pwned(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "⚠ Error accessing breach API"
        hashes = response.text.splitlines()
        for line in hashes:
            if suffix in line:
                count = line.split(":")[1]
                return f"⚠ Found in breaches {count} times"
        return "✅ Not found in known breaches"
    except:
        return "⚠ Could not connect to API"

# -------- Wordlist Generator --------
def generate_wordlist(base_words):
    patterns = []
    for word in base_words:
        word = word.strip()
        if not word:
            continue
        patterns.extend([
            word,
            word.capitalize(),
            word.upper(),
            word[::-1],
            word + "123",
            word + "2025",
            word + "@123",
            "@" + word,
            word + "!",
            word.replace('a','@').replace('s','$').replace('i','1').replace('o','0')
        ])
    return list(set(patterns))

# -------- Streamlit UI --------
st.set_page_config(page_title="Password Strength Analyzer", page_icon="🔐", layout="centered")
st.title("🔐 Password Strength Analyzer + Wordlist Generator")
st.caption("Built using Python + Streamlit")

username = st.text_input("Enter your name or email (optional)")
password = st.text_input("Enter password to analyze", type="password")

if password:
    z_result = zxcvbn(password)
    base_percent = (z_result['score'] + 1) * 10
    passed_rules = count_passed_rules(password, username)
    rule_percent = (passed_rules / 9) * 50
    strength = round(base_percent + rule_percent, 2)

    st.markdown("### 🔍 Password Analysis")
    st.progress(strength / 100)
    st.markdown(f"**Strength Score:** `{strength}%`")

    if strength >= 85:
        st.success("🟢 Strong password")
    elif strength >= 60:
        st.warning("🟡 Moderate password — can be improved")
    else:
        st.error("🔴 Weak password — risky to use")

    # Suggestions
    issues = validate_password(password, username)
    if issues:
        st.markdown("### ⚠ Suggestions:")
        for i in issues:
            st.write(f"- {i}")
    else:
        st.success("✅ All rule-based checks passed!")

    # Breach check
    with st.spinner("Checking data breach database..."):
        leak_status = check_pwned(password)
    st.markdown(f"### 📡 Breach Check:\n{leak_status}")

# -------- Wordlist Generator Section --------
st.markdown("---")
st.header("🧰 Custom Wordlist Generator")

base = st.text_area("Enter base words (name, pet, hobby, etc. — separated by comma or space):")
if st.button("🔄 Generate Wordlist"):
    base_words = base.replace(",", " ").split()
    wordlist = generate_wordlist(base_words)
    
    st.subheader(f"Generated Wordlist ({len(wordlist)} words)")
    st.code("\n".join(wordlist), language="text")

    # Prepare downloadable file
    wordlist_str = "\n".join(wordlist)
    wordlist_bytes = io.BytesIO(wordlist_str.encode("utf-8"))
    st.download_button("💾 Download Wordlist (.txt)", wordlist_bytes, file_name="custom_wordlist.txt")
