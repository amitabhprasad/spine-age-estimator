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
def ask_question(q, options, help_text=None):
    return st.radio(q, options, help=help_text, horizontal=False)

answers = []
section_scores = {"Core and Posture": 0, "Strength and Balance": 0, "Recovery and Lifestyle": 0}

st.markdown("### 🧍 Core and Posture")
core_questions = [
    ("How do you feel when you get out of bed in the morning?", "Assesses spinal stiffness and general mobility after rest."),
    ("Can you hold a deep squat for 60 seconds without discomfort?", "Evaluates hip, ankle, and lumbar mobility under load."),
    ("Can you rotate your upper body and look fully over each shoulder without pain?", "Checks thoracic and cervical spine rotation capacity.")
]
for q, hint in core_questions:
    a = ask_question(q, ["A) No stiffness", "B) Some stiffness", "C) Pain or difficulty"], help_text=hint)
    section_scores["Core and Posture"] += 2 if a.startswith("A") else 1 if a.startswith("B") else 0
    answers.append(a)

st.markdown("### 🏋️ Strength and Balance")
strength_questions = [
    ("Can you perform 5 jump squats and box jumps (minimum 12–16 inches) without fear or back/knee pain?", "Assesses explosive power, spinal load tolerance, and confidence."),
    ("Can you perform standing knee drives (15 per leg) and maintain posture without compensations?", "Tests core stability, hip flexor strength, and balance."),
    ("Can you stand on one leg (eyes closed) for at least 30 seconds on both legs?", "Evaluates proprioception and lower body neural balance.")
]
for q, hint in strength_questions:
    a = ask_question(q, ["A) Yes", "B) Somewhat", "C) No"], help_text=hint)
    section_scores["Strength and Balance"] += 2 if a.startswith("A") else 1 if a.startswith("B") else 0
    answers.append(a)

st.markdown("### 🛌 Recovery and Lifestyle")
recovery_questions = [
    ("Do you regularly feel back soreness after long sitting or lifting?", "Detects postural fatigue or disc pressure buildup."),
    ("Do you do specific exercises to decompress your spine (e.g., hangs, McKenzie extensions)?", "Indicates proactive recovery and spinal unloading habits."),
    ("Do you sleep on a supportive mattress with good posture?", "Evaluates nighttime spinal recovery environment."),
    ("Do you consciously maintain upright posture while working/sitting?", "Assesses awareness and effort in posture maintenance."),
    ("Have you had back pain lasting more than a week in the past year?", "Looks for chronicity and frequency of spinal stress episodes.")
]
for q, hint in recovery_questions:
    if "soreness" in q:
        options = [
            "A) Rarely or never feel soreness",
            "B) Occasionally feel mild soreness",
            "C) Frequently feel moderate or severe soreness"
        ]
    else:
        options = [
            "A) Consistently / Always",
            "B) Sometimes",
            "C) Rarely or Never"
        ]
    a = ask_question(q, options, help_text=hint)
    section_scores["Recovery and Lifestyle"] += 2 if a.startswith("A") else 1 if a.startswith("B") else 0
    answers.append(a)

if st.button("🔍 Calculate My Spine Age"):
    total_score = sum(section_scores.values())

    # Max score = 22
    # Adjusted mapping based on actual age brackets
    if actual_age <= 18:
        if total_score >= 20:
            spine_age = 12
        elif total_score >= 17:
            spine_age = 15
        elif total_score >= 14:
            spine_age = 18
        else:
            spine_age = 22
    elif actual_age >= 50 and total_score >= 21:
        spine_age = 30  # Cap athletic aging reversal for older users
    else:
        if total_score >= 21:
            spine_age = 16
        elif total_score >= 19:
            spine_age = 24
        elif total_score >= 17:
            spine_age = 30
        elif total_score >= 14:
            spine_age = 40
        elif total_score >= 11:
            spine_age = 50
        else:
            spine_age = 60

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

    # Summary of strengths/weaknesses
    st.markdown("### 💡 Strengths & Weaknesses Summary")
    for section, score in section_scores.items():
        if section == "Recovery and Lifestyle":
            max_score = 10
        else:
            max_score = 6
        percent = (score / max_score) * 100
        if percent >= 80:
            st.success(f"✅ {section}: Excellent")
        elif percent >= 50:
            st.warning(f"⚠️ {section}: Moderate – Room for improvement")
        else:
            st.error(f"🚨 {section}: Needs attention")

        # What This Checks Section
    st.markdown("### 🔍 What This Assessment Checks")
    st.markdown("""⚠️ **Disclaimer:** This tool is for general educational and wellness purposes only. It is not a substitute for professional medical diagnosis or treatment. Please consult your physician or physical therapist for any persistent or serious spinal concerns.

---

- **Core and Posture**: Evaluates spinal stiffness, rotation, and squat ability to detect early degeneration or joint limitations.
- **Strength and Balance**: Tests dynamic movements like jumps and one-leg balance to assess power, control, and proprioception.
- **Recovery and Lifestyle**: Captures daily spine care, sleep posture, postural awareness, and history of chronic stress.
""")
