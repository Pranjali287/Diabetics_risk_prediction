import streamlit as st
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Pink & White Theme
st.markdown("""
    <style>
    /* Main Background: Soft White to Light Pink Gradient */
    .stApp {
        background: linear-gradient(180deg, #fff0f6 0%, #ffe3e3 100%);
        color: #880e4f; /* Dark Pink Text for visibility instead of black */
    }
    
    /* Headers (Strong Pink) */
    h1, h2, h3, h4, h5, h6 {
        color: #d81b60 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Text Inputs & Select Boxes Labels */
    label, .stMarkdown p {
        color: #880e4f !important; /* Dark Pink text */
        font-weight: 500;
    }

    /* Sidebar Background (Distinct Baby Pink) */
    [data-testid="stSidebar"] {
        background-color: #ffd1dc; /* Baby Pink */
        border-right: 2px solid #f8bbd0;
    }
    
    /* Primary Buttons (Hot Pink) - Larger touch target */
    div.stButton > button:first-child {
        background-color: #ec407a;
        color: white;
        border: 2px solid #d81b60;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.3rem !important; /* Larger text */
        padding: 0.8rem 2rem !important; /* Larger button */
        height: auto !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* Slight shadow for depth */
    }
    
    div.stButton > button:first-child:hover {
        background-color: #d81b60;
        color: white;
        border-color: #ad1457;
        transform: scale(1.02); /* Slight grow effect */
    }
    
    /* Input Fields Style - Low vision friendly */
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border-color: #ec407a !important; /* Stronger pink border */
        border-width: 2px !important;
        border-radius: 10px;
        color: #880e4f !important;
        height: 3.5rem !important; /* Much Taller inputs */
    }
    
    /* Ensure the actual input text is visible and large */
    input[type="number"], input[type="text"] {
        color: #880e4f !important;
        background-color: transparent !important;
        font-size: 1.3rem !important; /* Much Larger input text */
        font-weight: 700 !important;
    }
    
    /* Number input step arrows - make them larger */
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        cursor: pointer;
        opacity: 1;
        transform: scale(1.5);
        margin-left: 10px;
    }

    /* Select box text */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #880e4f !important;
        border-color: #ec407a !important;
        height: 3.5rem !important;
    }
    
    div[data-baseweb="select"] span {
        font-size: 1.3rem !important; /* Larger select text */
        font-weight: 700;
    }
    
    /* Dropdown menu items */
    li[role="option"] {
        color: #880e4f !important;
        background-color: #fff0f6 !important;
        font-size: 1.2rem !important;
        padding: 10px !important;
    }

    /* Metric Values - Very Large */
    [data-testid="stMetricValue"] {
        color: #c2185b !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }
    
    /* Info Alerts (Light Pink Background) */

    .stAlert {
        background-color: #fff0f6;
        border: 1px solid #fcc2d7;
        color: #a61e4d;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logic from app.py ---
# 12 features (9 clinical + 3 genetic risk-allele counts)
FEATURES = [
    "Age", "BMI", "Glucose", "Insulin", "HOMA",
    "Leptin", "Adiponectin", "Resistin", "MCP.1",
    "RA_SNP1", "RA_SNP2", "RA_SNP3"
]

# Means and STDs chosen around clinically plausible ranges, to stabilize scaling
MEANS = np.array([
    48.0, 27.0, 110.0, 10.0, 2.7,
    15.0,  9.0,  8.0, 420.0,
     1.0,  1.0,  1.0
], dtype=float)

STDS = np.array([
    18.0, 6.0, 28.0, 5.0, 2.0,
     8.0, 4.0, 3.0, 120.0,
     0.7, 0.7, 0.7
], dtype=float)

# Coefficients: positive for risk-raising factors, negative for protective ones.
COEFS = np.array([
    0.18,   # Age
    0.35,   # BMI
    0.55,   # Glucose
    0.25,   # Insulin
    0.25,   # HOMA
    0.08,   # Leptin
   -0.30,   # Adiponectin (protective)
    0.20,   # Resistin
    0.10,   # MCP.1
    0.40,   # RA_SNP1
    0.32,   # RA_SNP2
    0.28    # RA_SNP3
], dtype=float)

# Intercept such that a "typical" profile lands near mid risk (~40–50%)
INTERCEPT = -0.35

def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + np.exp(-z))

def predict_risk(inputs):
    # Order the inputs according to FEATURES
    vals = [inputs.get(f, 0.0) for f in FEATURES]
    x = np.array(vals, dtype=float)
    
    # Standardize and score
    # (x - mean) / std * coef + intercept
    z = np.dot((x - MEANS) / STDS, COEFS) + INTERCEPT
    p = float(sigmoid(z))
    return p

# --- UI ---

st.title("🧬 Diabetes Risk & Genetic Score Prediction")
st.markdown("""
This application predicts the risk of Type 2 Diabetes combining **clinical markers** and **genetic risk factors**.  
Please fill out the form below to get a detailed risk assessment and personalized suggestions.
""")

with st.form("prediction_form"):
    st.subheader("📝 Clinical Markers")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age (years)", min_value=0, max_value=120, value=0, help="Patient's age in years.")
        bmi = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=60.0, value=0.0, step=0.1, help="Body Mass Index. Normal range is 18.5 - 24.9.")
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=400.0, value=0.0, step=1.0, help="Fasting blood glucose level. Normal < 100 mg/dL.")
    
    with col2:
        insulin = st.number_input("Insulin (µU/mL)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, help="Fasting insulin level. Normal range 2.6 - 24.9 µU/mL.")
        homa = st.number_input("HOMA-IR", min_value=0.0, max_value=20.0, value=0.0, step=0.1, help="Homeostatic Model Assessment for Insulin Resistance. Normal < 1.0.")
        leptin = st.number_input("Leptin (ng/mL)", min_value=0.0, max_value=200.0, value=0.0, step=0.1, help="Hormone involved in energy regulation.")

    with col3:
        adiponectin = st.number_input("Adiponectin (µg/mL)", min_value=0.0, max_value=50.0, value=0.0, step=0.1, help="Protein hormone which modulates metabolic processes. Higher is generally better.")
        resistin = st.number_input("Resistin (ng/mL)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, help="Hormone linked to obesity and insulin resistance.")
        mcp1 = st.number_input("MCP-1 (pg/mL)", min_value=0.0, max_value=2000.0, value=0.0, step=1.0, help="Monocyte Chemoattractant Protein-1, an inflammatory marker.")

    st.subheader("🧬 Genetic Risk Factors")
    st.info("Select the number of risk alleles for each SNP variant (0, 1, or 2).", icon="ℹ️")
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        ra_snp1 = st.selectbox("RA SNP1 Count", [0, 1, 2], index=0)
    with g_col2:
        ra_snp2 = st.selectbox("RA SNP2 Count", [0, 1, 2], index=0)
    with g_col3:
        ra_snp3 = st.selectbox("RA SNP3 Count", [0, 1, 2], index=0)

    submit_button = st.form_submit_button("🔍 Analyze Risk", type="primary")

# Collect inputs
input_data = {
    "Age": age,
    "BMI": bmi,
    "Glucose": glucose,
    "Insulin": insulin,
    "HOMA": homa,
    "Leptin": leptin,
    "Adiponectin": adiponectin,
    "Resistin": resistin,
    "MCP.1": mcp1,
    "RA_SNP1": ra_snp1,
    "RA_SNP2": ra_snp2,
    "RA_SNP3": ra_snp3
}

def get_detailed_suggestions(data, risk_pct):
    suggestions = []
    
    # Risk Level Base Advice
    if risk_pct < 34:
        suggestions.append(("🟢", "Your risk is **Low**. Maintain your current healthy lifestyle habits."))
    elif risk_pct < 67:
        suggestions.append(("🟠", "Your risk is **Moderate**. Proactive lifestyle changes can help lower this risk."))
    else:
        suggestions.append(("🔴", "Your risk is **High**. We strongly recommend consulting a healthcare provider."))

    # Specific Marker Advice
    if data["BMI"] >= 30:
        suggestions.append(("⚖️", "**BMI**: You are in the obese range. Aim for gradual weight loss through diet and exercise."))
    elif data["BMI"] >= 25:
        suggestions.append(("⚖️", "**BMI**: You are in the overweight range. Losing even 5-10% of body weight can significantly reduce risk."))
        
    if data["Glucose"] >= 126:
        suggestions.append(("🩸", "**Glucose**: Your fasting glucose is high (>= 126 mg/dL). This is a strong indicator of diabetes/pre-diabetes."))
    elif data["Glucose"] >= 100:
        suggestions.append(("🩸", "**Glucose**: Your glucose is in the pre-diabetic range (100-125 mg/dL). Reduce sugar and refined carb intake."))
        
    if data["HOMA"] > 2.0:
        suggestions.append(("📉", "**HOMA-IR**: Indicates insulin resistance. Regular physical activity (30 mins/day) helps improve insulin sensitivity."))

    if data["Adiponectin"] < 10:
        suggestions.append(("🥑", "**Adiponectin**: Your levels are low. Increasing intake of healthy fats (avocados, nuts, fish) may help."))

    return suggestions

# Prediction
if submit_button:
    probability = predict_risk(input_data)
    risk_percent = round(probability * 100, 2)
    # Determine risk category
    if risk_percent < 34:
        risk_type = "Low"
        color_class = "st-emotion-cache-1wivap2" # green-ish default
    elif risk_percent < 67:
        risk_type = "Medium"
    else:
        risk_type = "High"

    st.divider()
    st.header("📊 Assessment Results")

    # Top level metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Probability", f"{risk_percent}%", delta=None)
    m2.metric("Risk Category", risk_type)
    
    # Colored progress bar
    bar_color = "red" if risk_type == "High" else "orange" if risk_type == "Medium" else "green"
    st.progress(risk_percent / 100, text=f"Risk Probability: {risk_percent}%")
    
    # Detailed Suggestions Section
    st.subheader("💡 Personalized Suggestions")
    
    suggestions = get_detailed_suggestions(input_data, risk_percent)
    
    for icon, tip in suggestions:
        st.info(f"{icon} {tip}")

    with st.expander("🔬 View Detailed Raw Data"):
        st.json(input_data)

