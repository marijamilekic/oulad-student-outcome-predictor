"""
Streamlit forma za baseline model

Pokretanje streamlit run app/streamlit_app.py
"""

import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.title("Predikcija Rizika Odustajanja Studenata")

with st.form("student_form"):
    code_module = st.selectbox("Courses", ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"])
    gender = st.selectbox("Gender", ["M", "F"])
    region = st.selectbox("Region", ['East Anglian Region', 'Scotland', 'North Western Region', 'South East Region', 'West Midlands Region', 'Wales', 'North Region', 'South Region', 'Ireland', 
                                     'South West Region', 'East Midlands Region', 'Yorkshire Region', 'London Region'])
    highest_education = st.selectbox("Education", ["No Formal quals", "Lower Than A Level", "A Level or Equivalent", "HE Qualification", "Post Graduate Qualification"])
    imd_band = st.selectbox("IMD band", ['0-10%', '10-20', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%' , 'nan'])
    age_band = st.selectbox("Age band", ["0-35", "35-55", "55<="])
    disability = st.selectbox("Disability", ["N", "Y"])
    num_of_prev_attempts = st.number_input("Number of previous attempts", min_value=0, value=0)
    studied_credits = st.number_input("Studied credits", min_value=1, value=60)
    module_presentation_length = st.number_input(" Module presentation length (days)", min_value=1, value=268)
    date_registration = st.number_input("Days before the course starts (negative number)", value=-50, max_value=0)

    submitted = st.form_submit_button("Submit")

if submitted:
    payload = {
        "code_module": code_module,
        "gender": gender,
        "region": region,
        "highest_education": highest_education,
        "imd_band": imd_band,
        "age_band": age_band,
        "disability": disability,
        "num_of_prev_attempts": num_of_prev_attempts,
        "studied_credits": studied_credits,
        "module_presentation_length": module_presentation_length,
        "date_registration": date_registration,
    }

    response = requests.post(f"{API_URL}/predict", json=payload)
    result = response.json()

    probability = result["at_risk_probability"]
    st.metric("Verovatnoca rizika", f"{probability:.1%}")

    if result["at_risk_prediction"] == 1:
        st.warning("Student je verovatno u riziku.")
    else:
        st.success("Student verovatno nece biti u riziku.")