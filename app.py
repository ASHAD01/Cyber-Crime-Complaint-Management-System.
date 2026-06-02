import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cyber Crime Control Room", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0b1120, #172554);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
    border-right: 2px solid #00d4ff;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Headings */
h1 {
    color: #00d4ff !important;
    text-align: center;
    font-weight: 800;
}
h2, h3 {
    color: #38bdf8 !important;
    font-weight: 700;
}

/* Text */
p, label, span {
    color: white !important;
}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
    border-radius: 10px;
    border: 2px solid #00d4ff !important;
}

/* Buttons */
.stButton>button, .stDownloadButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
    box-shadow: 0px 4px 12px rgba(0,198,255,0.4) !important;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    transform: scale(1.05);
}

/* Dashboard Metric Cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e40af, #2563eb) !important;
    border: 2px solid #38bdf8 !important;
    padding: 20px !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    text-align: center !important;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div {
    color: white !important;
    font-weight: bold !important;
}

/* Table */
[data-testid="stDataFrame"] {
    background: white !important;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

/* Alerts */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1>🔐 Officer Login</h1>", unsafe_allow_html=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()

# ---------------- SESSION ----------------
if "cases" not in st.session_state:
    st.session_state.cases = []

if "ack_ids" not in st.session_state:
    st.session_state.ack_ids = []

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🚔 Cyber Crime Control Room")
page = st.sidebar.radio("Navigation", ["Dashboard", "Register Case", "Case Status"])
# ---------------- CLASSIFICATION ----------------
def classify(text):
    text = text.lower()

    social_media_words = [
        "instagram", "insta", "facebook", "fb", "whatsapp", "gmail",
        "telegram", "twitter", "x", "snapchat", "linkedin", "youtube",
        "account hack", "social media hack", "id hack", "account stolen",
        "account disabled", "account blocked", "otp issue"
    ]

    financial_words = [
        "upi", "bank", "money", "paisa", "cash", "fraud", "scam",
        "payment", "transaction", "debit", "credit", "atm", "loan",
        "refund", "wallet", "net banking", "phishing", "card fraud",
        "online shopping fraud", "investment fraud"
    ]

    hacking_words = [
        "hack", "hacked", "hacking", "device hack", "phone hack",
        "mobile hack", "telephone hack", "system hack", "laptop hack",
        "computer hack", "email hack", "website hack"
    ]

    mobile_words = [
        "lost phone", "stolen phone", "mobile lost", "phone lost",
        "phone stolen", "mobile stolen", "mobile gum", "phone gum",
        "mobile missing", "phone missing", "imei", "lost mobile",
        "stolen mobile", "gum phone", "gum mobile", "loss phone",
        "loss mobile"
    ]

    blackmail_words = [
        "blackmail", "threat", "dhamki", "extortion", "harass",
        "harassment", "abuse", "abusive", "ransom", "bully",
        "bullying", "sexual threat", "kill", "murder threat"
    ]

    if any(word in text for word in social_media_words):
        return "Social Media Crime"
    elif any(word in text for word in financial_words):
        return "Financial Fraud"
    elif any(word in text for word in hacking_words):
        return "Hacking"
    elif any(word in text for word in mobile_words):
        return "CEIR Mobile Case"
    elif any(word in text for word in blackmail_words):
        return "Cyber Blackmail"
    return "Other Cyber Crime"

# ---------------- SEVERITY ----------------
def severity(cat):
    if cat in ["Hacking", "Financial Fraud", "Cyber Blackmail"]:
        return "HIGH"
    elif cat == "Social Media Crime":
        return "MEDIUM"
    return "LOW"

# ---------------- OFFICER ----------------
def assign_officer(cat):
    return {
        "Hacking": "JKPSI Ankush Sharma",
        "CEIR Mobile Case": "JKPSI Rakesh Kumar",
        "Social Media Crime": "Inspector Ajit Singh",
        "Financial Fraud": "Inspector Bhupinder Singh",
        "Cyber Blackmail": "DSP Rohit Chadyal",
        "Other Cyber Crime": "Duty Officer"
    }.get(cat, "Duty Officer")

# ---------------- CASE ID ----------------
def generate_case_id():
    return f"CYB-{len(st.session_state.cases)+1:04d}"

# ---------------- WORKFLOW ----------------
def investigation_steps(cat):
    return {
        "Hacking": [
            "Receive and register the complaint in Cyber Crime Portal / Police Station record.",
            "Immediately secure the victim's mobile, laptop or affected device to prevent further damage.",
            "Send the device to the Forensic Department / Cyber Forensic Lab for malware analysis and evidence extraction.",
            "Check whether spyware, remote access apps, phishing links or suspicious APK files are installed.",
            "Collect browser history, suspicious emails, SMS logs, app logs and screenshots.",
            "Trace suspicious IP addresses, VPN logs and login history.",
            "Request CAF (Customer Application Form) and CDR (Call Detail Record) from telecom companies if required.",
            "Analyze recovered digital evidence and identify suspect location through IP / tower dump / wireless signals.",
            "Call suspect for questioning or conduct raid if evidence is confirmed.",
            "Secure victim’s account/device and provide prevention guidance."
        ],

        "Financial Fraud": [
            "Immediately report the complaint on National Cyber Crime Portal / Helpline 1930.",
            "Contact concerned bank / UPI / wallet company to freeze beneficiary account.",
            "Track the money trail from one account to another.",
            "Collect bank statement, transaction ID, screenshots and payment proof.",
            "Request beneficiary KYC details from bank.",
            "Obtain CAF/CDR of linked mobile numbers from telecom companies.",
            "Trace suspect location through IP logs, ATM CCTV footage and wireless signals.",
            "Issue legal notice to banks/payment gateways.",
            "Call suspect for investigation / recovery proceedings.",
            "Prepare report and initiate legal action."
        ],

        "Social Media Crime": [
            "Register complaint and collect screenshots, profile links, chats and all digital evidence.",
            "Identify whether account is hacked, cloned, fake or used for fraud/abuse.",
            "Send official notice to Meta / Instagram / Facebook / WhatsApp / Twitter / Snapchat / Google etc.",
            "Request login IP logs, registered mobile number, registered email ID and device details.",
            "Obtain account creation details and activity logs from concerned platform.",
            "If mobile number found, obtain CAF and CDR from telecom company.",
            "Trace live/suspect location using tower location and wireless signals.",
            "Call suspect to Cyber Police Station for questioning.",
            "Recover the account / disable fake account / remove objectionable content.",
            "Provide cyber safety awareness to complainant."
        ],

        "Cyber Blackmail": [
            "Collect screenshots, chats, audio/video recordings and profile details.",
            "Preserve digital evidence under cyber forensic procedure.",
            "Identify suspect through social media logs / IP address / mobile number.",
            "Send legal notice to social media platform for account details.",
            "Obtain CAF/CDR from telecom operator if number involved.",
            "Trace suspect location through wireless signals / tower location.",
            "Call suspect immediately and initiate strict legal action.",
            "Provide safety and counseling support to victim."
        ],

        "CEIR Mobile Case": [
            "Register complaint and collect IMEI number, invoice and mobile details.",
            "Block the IMEI through CEIR Portal immediately.",
            "Put the mobile on active tracking through CEIR system.",
            "Request CAF and CDR of SIM inserted in stolen/lost phone.",
            "Trace current location through telecom tower and wireless signals.",
            "Coordinate with local police station / field staff for recovery.",
            "Call suspect / current user to Cyber Police Station.",
            "Recover the mobile and verify ownership documents.",
            "Hand over recovered device to rightful owner."
        ],

        "Other Cyber Crime": [
            "Collect complete complaint details and evidence.",
            "Analyze the nature of the cyber offence.",
            "Trace digital evidence and suspect details.",
            "Take legal and technical action accordingly."
        ]
    }.get(cat, ["Investigate"])

# ---------------- REGISTER PAGE ----------------
if page == "Register Case":
    st.markdown("<h1>📝 Register Cyber Crime Case</h1>", unsafe_allow_html=True)

    text = st.text_area("Enter Complaint")
    ack_no = st.text_input("Enter Acknowledgement Number (10+ chars)")

    if st.button("Analyze Case"):

        if len(ack_no) < 10:
            st.error("❌ Acknowledgement number must be at least 10 characters (letters + numbers)")
            st.stop()

        if text.strip():

            category = classify(text)
            risk = severity(category)
            officer = assign_officer(category)
            steps = investigation_steps(category)

            case_id = generate_case_id()
            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            st.session_state.cases.append({
                "case_id": case_id,
                "ack_no": ack_no,
                "category": category,
                "severity": risk,
                "officer": officer,
                "time": time_now,
                "status": "pending"
            })

            st.success("✅ Case Registered Successfully")
            st.info(f"Case ID: {case_id} | Category: {category} | Severity: {risk}")
            st.info(f"Acknowledgement No: {ack_no}")
            st.info(f"Officer: {officer} | Time: {time_now}")

            st.markdown("### 🛡 Investigation Steps")
            for i, step in enumerate(steps):
                st.write(f"{i+1}. {step}")


# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.markdown("<h1>📊 Cyber Crime Dashboard</h1>", unsafe_allow_html=True)

    if st.session_state.cases:
        df = pd.DataFrame(st.session_state.cases)

        total = len(df)
        high = len(df[df["severity"] == "HIGH"])
        medium = len(df[df["severity"] == "MEDIUM"])
        low = len(df[df["severity"] == "LOW"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Cases", total)
        c2.metric("High Risk", high)
        c3.metric("Medium Risk", medium)
        c4.metric("Low Risk", low)

        st.markdown("### 📊 Crime Analytics")
        st.bar_chart(df["category"].value_counts(), use_container_width=True)

        st.markdown("### 🔍 Filter Cases")
        category_filter = st.selectbox("Select Category", ["All"] + list(df["category"].unique()))

        if category_filter != "All":
            df = df[df["category"] == category_filter]

        def highlight(val):
            if val == "HIGH":
                return "background-color:red;color:white"
            elif val == "MEDIUM":
                return "background-color:orange;color:black"
            else:
                return "background-color:lightgreen;color:black"

        st.markdown("### 📋 Case Register")
        st.dataframe(df.style.map(highlight, subset=["severity"]), use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Report", csv, "cyber_report.csv", "text/csv")
        html = df.to_html(index=False)
        st.download_button("🖨 Print Report (Open & Print)", html, "report.html", "text/html")
    else:
        st.info("No cases available yet")


# ---------------- CASE STATUS ----------------
if page == "Case Status":
    st.markdown("<h1>📌 Track Case Status</h1>", unsafe_allow_html=True)

    case_id_search = st.text_input("Enter Case ID")
    ack_search = st.text_input("Enter Acknowledgement Number")

    found = None

    if case_id_search or ack_search:

        for case in st.session_state.cases:

            if (
                (case_id_search and case["case_id"].lower() == case_id_search.lower())
                or
                (ack_search and case.get("ack_no", "").lower() == ack_search.lower())
            ):
                found = case
                break

        if found:
            st.success("✅ Case Found")

            st.info(f"Case ID: {found['case_id']}")
            st.info(f"Acknowledgement No: {found.get('ack_no','')}")
            st.info(f"Category: {found['category']}")
            st.info(f"Severity: {found['severity']}")
            st.info(f"Assigned Officer: {found['officer']}")
            st.info(f"Registered Time: {found['time']}")

            status_options = ["Pending", "Under Investigation", "Resolved"]

            current_status = found["status"].title()

            status = st.radio(
                "Update Case Status",
                status_options,
                index=status_options.index(current_status) if current_status in status_options else 0
            )

            found["status"] = status

            st.warning(f"Current Status: {found['status']}")

        else:
            st.error("❌ Case not found")