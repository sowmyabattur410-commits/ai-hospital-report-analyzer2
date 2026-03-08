import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Medical Report Analyzer", layout="wide")

# ---------------- SESSION STATES ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "section" not in st.session_state:
    st.session_state.section = "dashboard"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf1_data" not in st.session_state:
    st.session_state.pdf1_data = None

if "pdf2_data" not in st.session_state:
    st.session_state.pdf2_data = None

if "user_info" not in st.session_state:
    st.session_state.user_info = {"name":"","email":"","hospital":""}

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp{
background: linear-gradient(145deg, #f0f4f8, #d9e2f3);
font-family: "Segoe UI", sans-serif;
}

.title{
font-size:42px;
font-weight:700;
text-align:center;
color:#1a2b4c;
}

.subtitle{
text-align:center;
color:#4b5d7c;
margin-bottom:30px;
font-size:18px;
}

.card{
background:white;
padding:30px;
border-radius:20px;
box-shadow:0 10px 25px rgba(0,0,0,0.08);
margin-bottom:25px;
transition:0.3s;
}

.card:hover{
transform: translateY(-3px);
box-shadow:0 12px 30px rgba(0,0,0,0.15);
}

.stButton > button{
background: linear-gradient(135deg,#4A6CF7,#6E8BFF);
color:white;
border:none;
padding:14px 25px;
border-radius:12px;
font-size:17px;
font-weight:600;
width:100%;
transition:0.3s;
}

.stButton > button:hover{
transform:scale(1.05);
box-shadow:0 8px 25px rgba(74,108,247,0.45);
}

button:disabled {
background: #b0c4de !important;
color: #fff !important;
cursor: not-allowed !important;
}

.dataframe th {
background-color: #4A6CF7 !important;
color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.markdown('<div class="title">Welcome to AI Medical Report Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Please login to continue</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    name = st.text_input("Enter your Name", key="login_name")
    email = st.text_input("Enter your Email", key="login_email")
    hospital = st.text_input("Enter your Hospital Name", key="login_hospital")
    if st.button("Login", key="login_button"):
        if name and email and hospital:
            st.session_state.user_info = {"name": name, "email": email, "hospital": hospital}
            st.session_state.page = "home"
            st.success(f"Welcome {name}! You are now logged in.")
            st.rerun()
        else:
            st.warning("Please fill all fields to continue.")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- HOME PAGE ----------------
elif st.session_state.page == "home":
    st.markdown(f'<div class="title">Hello, {st.session_state.user_info["name"]}!</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload your medical report and get AI insights</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Medical Report", type=["pdf"], key="home_upload")
    if st.button("Analyze Report", key="home_analyze_button"):
        if uploaded_file:
            st.session_state.page = "analysis"
            st.rerun()
        else:
            st.warning("Please upload a medical report first")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- ANALYSIS PAGE ----------------
elif st.session_state.page == "analysis":
    st.markdown(f"## 📊 Medical Report Analysis for {st.session_state.user_info['name']}")

    nav1, nav2, nav3, nav4 = st.columns(4)
    with nav1: 
        if st.button("Dashboard", key="nav_dashboard"): st.session_state.section = "dashboard"
    with nav2: 
        if st.button("Detailed Report", key="nav_detail"): st.session_state.section = "detail"
    with nav3: 
        if st.button("AI Summary", key="nav_summary"): st.session_state.section = "summary"
    with nav4: 
        if st.button("Compare Reports", key="nav_compare"): st.session_state.section = "compare"

    st.write("")

    # ---------------- DASHBOARD ----------------
    if st.session_state.section == "dashboard":
        st.subheader("Health Overview")
        col1,col2,col3 = st.columns(3)
        with col1: st.metric("Hemoglobin","13.5","Normal")
        with col2: st.metric("Cholesterol","210","High")
        with col3: st.metric("Glucose","90","Normal")
        st.info("Overview of key health indicators extracted from the medical report.")

        st.markdown("### 📈 Key Health Indicators")
        indicators = ["Hemoglobin","Cholesterol","Glucose"]
        values = [13.5,210,90]
        fig, ax = plt.subplots()
        ax.bar(indicators, values, color=['#4CAF50','#F44336','#4CAF50'])
        ax.set_ylabel("Value")
        st.pyplot(fig)

    # ---------------- DETAILED REPORT ----------------
    elif st.session_state.section == "detail":
        st.subheader("Detailed Medical Report")
        data = {
            "Test Name":["Hemoglobin","Cholesterol","Glucose","Blood Pressure","Vitamin D","Calcium","White Blood Cells"],
            "Result":["13.5 g/dL","210 mg/dL","90 mg/dL","120/80","22 ng/mL","9.1 mg/dL","7000 cells/mcL"],
            "Normal Range":["12 - 16 g/dL","< 200 mg/dL","70 - 100 mg/dL","120/80","30 - 100 ng/mL","8.6 - 10.2 mg/dL","4000 - 11000"],
            "Status":["Normal","High","Normal","Normal","Low","Normal","Normal"]
        }
        df = pd.DataFrame(data)
        def highlight_status(val):
            if val in ["High","Low"]: return "color:#F44336; font-weight:bold"
            else: return "color:#4CAF50; font-weight:bold"
        styled_df = df.style.applymap(highlight_status, subset=["Status"])
        st.dataframe(styled_df, use_container_width=True)

        st.markdown("### ⚠ Important Observations")
        st.markdown("""
🔴 **Cholesterol is higher than normal**  
High cholesterol may increase the risk of heart disease.

🔴 **Vitamin D is low**  
Low vitamin D can affect bone health and immunity.
""")

    # ---------------- AI SUMMARY ----------------
    elif st.session_state.section == "summary":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#1a2b4c; text-align:center;">🤖 AI Summary</h2>', unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center; color:#4b5d7c; font-size:16px;">
        Summary of your medical report.
        </p>
        """, unsafe_allow_html=True)
        summary_text = """
- Most parameters are within the normal range. ✅
- Cholesterol is slightly high. ⚠️
- Vitamin D is slightly low. ⚠️
- Hemoglobin, Glucose, Calcium, and WBC levels are normal. ✅
"""
        st.markdown(f'<pre style="font-size:16px; line-height:1.6; color:#333;">{summary_text}</pre>', unsafe_allow_html=True)
        st.markdown('<div style="background:#e3f2fd; padding:20px; border-radius:12px; margin-top:20px;">', unsafe_allow_html=True)
        st.markdown("""
        <strong>Recommendations:</strong>
        <ul style="line-height:1.6;">
            <li>Reduce intake of fatty foods to manage cholesterol.</li>
            <li>Increase sunlight exposure and Vitamin D rich foods.</li>
            <li>Maintain a balanced diet and regular exercise.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- COMPARE REPORTS ----------------
    elif st.session_state.section == "compare":
        st.subheader("Compare Medical Reports")
        col1,col2 = st.columns(2)
        with col1: pdf1 = st.file_uploader("Upload PDF 1", key="pdf1_upload")
        with col2: pdf2 = st.file_uploader("Upload PDF 2", key="pdf2_upload")
        if pdf1: st.session_state.pdf1_data = pdf1
        if pdf2: st.session_state.pdf2_data = pdf2
        compare_enabled = st.session_state.pdf1_data and st.session_state.pdf2_data
        if st.button("Compare Reports", key="compare_button", disabled=not compare_enabled):
            labels = ["Hemoglobin","Cholesterol","Glucose"]
            pdf1_vals = [13.5,210,90]
            pdf2_vals = [12.8,180,95]

            # Comparison Table
            st.markdown("### 🗂 Comparison Table")
            compare_df = pd.DataFrame({
                "Test Name": labels,
                "PDF 1": pdf1_vals,
                "PDF 2": pdf2_vals,
                "Change": [round(pdf2_vals[i]-pdf1_vals[i],1) for i in range(len(labels))]
            })
            def highlight_change(val):
                if val > 0: return "color:#F44336; font-weight:bold"
                elif val < 0: return "color:#4CAF50; font-weight:bold"
                else: return "color:black"
            styled_compare_df = compare_df.style.applymap(highlight_change, subset=["Change"])
            st.dataframe(styled_compare_df, use_container_width=True)

            # Summary of Changes
            st.markdown("### 📝 Summary of Changes")
            summary_lines = []
            for i in range(len(labels)):
                if pdf2_vals[i] > pdf1_vals[i]:
                    summary_lines.append(f"🔴 {labels[i]} increased from {pdf1_vals[i]} to {pdf2_vals[i]}.")
                elif pdf2_vals[i] < pdf1_vals[i]:
                    summary_lines.append(f"🟢 {labels[i]} decreased from {pdf1_vals[i]} to {pdf2_vals[i]}.")
                else:
                    summary_lines.append(f"⚪ {labels[i]} remained the same at {pdf1_vals[i]}.")
            st.markdown("<br>".join(summary_lines), unsafe_allow_html=True)

            # Comparison Graph
            fig, ax = plt.subplots()
            x = np.arange(len(labels))
            width = 0.35
            ax.bar(x - width/2, pdf1_vals, width, label="PDF 1", color="#4A6CF7")
            ax.bar(x + width/2, pdf2_vals, width, label="PDF 2", color="#FF9800")
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.set_ylabel("Value")
            ax.set_title("Comparison of Key Health Indicators")
            ax.legend()
            st.pyplot(fig)
            st.success("Comparison completed.")

    if st.button("⬅ Back to Home", key="back_home"):
        st.session_state.page = "home"
        st.rerun()