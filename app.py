# app.py - Spine Age Estimator (Enhanced Version with Visualization, PDF, Progress Tracker)

import streamlit as st
import matplotlib.pyplot as plt
import datetime
import os
from fpdf import FPDF

st.set_page_config(page_title="Functional Spine Age Estimator", layout="centered")
st.title("🧬 Functional Spine Age Estimator")
st.markdown("Answer these questions to find your functional spine age and compare it with your actual age. We assess your posture, stability, flexibility, and loading tolerance.")

# Email and age input
email = st.text_input("📧 Enter your email to receive results (optional)")
actual_age = st.number_input("🎂 Your actual age (in years)", min_value=10, max_value=100, step=1)

# Question function
def ask_question(q, options):
    return st.radio(q, options, horizontal=False)

answers = []
section_scores = {"Core and Posture": 0, "Strength and Balance": 0, "Recovery and Lifestyle": 0}

st.markdown("### 🧍 Core and Posture")
for i, q in enumerate([
    "How do you feel when you get out of bed in the morning?",
    "Can you hold a deep squat for 60 seconds without discomfort?",
    "Can you rotate your upper body and look fully over each shoulder without pain?"  ]):
    a = ask_question(q, ["A) Yes / No stiffness", "B) Some stiffness", "C) Pain or difficulty"])
    section_scores["Core and Posture"] += 2 if a.startswith("A") else 1 if a.startswith("B") else 0
    answers.append(a)

st.markdown("### 🏋️ Strength and Balance")
for i, q in enumerate([
    "Can you perform 5 jump squats and box jumps (minimum 12–16 inches) without fear or back/knee pain?",
    "Can you perform standing knee drives (15 per leg) and maintain posture without compensations?",
    "Can you stand on one leg (eyes closed) for at least 30 seconds on both legs?"  ]):
    a = ask_question(q, ["A) Yes", "B) Somewhat", "C) No"])
    section_scores["Strength and Balance"] += 2 if a.startswith("A") else 1 if a.startswith("B") else 0
    answers.append(a)

st.markdown("### 🛌 Recovery and Lifestyle")
for i, q in enumerate([
    "Do you regularly feel back soreness after long sitting or lifting?",
    "Do you do specific exercises to decompress your spine (e.g., hangs, McKenzie extensions)?",
    "Do you sleep on a supportive mattress with good posture?",
    "Do you consciously maintain upright posture while working/sitting?",
    "Have you had back pain lasting more than a week in the past year?"  ]):
    a = ask_question(q, ["A) Yes / Rarely", "B) Sometimes", "C) No / Frequently"])
    section_scores["Recovery and Lifestyle"] += 2 if a.startswith("A") else 1 if a.startswith("B") else 0
    answers.append(a)

if st.button("🔍 Calculate My Spine Age"):
    total_score = sum(section_scores.values())

    if total_score >= 20:
        spine_age = 35
    elif total_score >= 16:
        spine_age = 45
    elif total_score >= 12:
        spine_age = 55
    else:
        spine_age = 65

    st.success(f"🎯 Your estimated functional spine age: {spine_age} years")

    if actual_age > 0:
        delta = actual_age - spine_age
        if delta > 5:
            st.markdown(f"🧪 Your spine is aging **better** than your body by {abs(delta)} years. 👏")
        elif delta < -5:
            st.markdown(f"⚠️ Your spine may be aging **faster** than your body by {abs(delta)} years.")
        else:
            st.markdown("✅ Your spine age matches your actual age. Great work!")

    # Visualize section scores
    st.markdown("### 📊 Section Score Overview")
    fig, ax = plt.subplots()
    ax.bar(section_scores.keys(), section_scores.values(), color=["#4CAF50", "#FFC107", "#2196F3"])
    ax.set_ylim(0, 10)
    ax.set_ylabel("Score out of 6/10")
    st.pyplot(fig)

    # PDF generation
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Functional Spine Age Report", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True)
        pdf.cell(200, 10, txt=f"Actual Age: {actual_age} years", ln=True)
        pdf.cell(200, 10, txt=f"Estimated Spine Age: {spine_age} years", ln=True)
        pdf.ln(5)
        for section, score in section_scores.items():
            pdf.cell(200, 10, txt=f"{section}: {score} / {10 if section=='Recovery and Lifestyle' else 6}", ln=True)
        pdf.output("spine_age_report.pdf")
        return "spine_age_report.pdf"

    if st.download_button("📄 Download My Report as PDF", data=open(generate_pdf(), "rb"), file_name="Spine_Age_Report.pdf"):
        st.success("📥 Your report has been downloaded!")

    # Optional: Save results for progress tracking
    if email:
        user_log = f"user_progress_{email.replace('@','_at_')}.txt"
        with open(user_log, "a") as f:
            f.write(f"{datetime.date.today()} | Age: {actual_age} | Spine Age: {spine_age} | Scores: {section_scores}\n")
        st.markdown(f"🗂️ Progress saved for: {email}")