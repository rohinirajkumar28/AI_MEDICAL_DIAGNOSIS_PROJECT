import pandas as pd
import streamlit as st
import base64
from collections import defaultdict

# Set Streamlit Page Config
st.set_page_config(page_title="AI Medical Diagnosis", page_icon="🩺", layout="wide")

# Function to encode the background image
def set_background_image(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    
    st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}
        .main-container {{
            max-width: 800px;
            margin: auto;
            background: rgba(255, 255, 255, 0.1); /* Transparent white */
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }}
        </style>
        """, unsafe_allow_html=True)

# Set background
set_background_image("background1.jpg")  # Make sure the image file exists in the directory

# Function to load and process the dataset
def load_dataset():
    df = pd.read_csv('Datasets.csv')
    df['Symptom'] = df['Symptom'].astype(str).str.strip().str.lower()
    df['Disease'] = df['Disease'].astype(str).str.strip()
    
    symptom_disease_map = defaultdict(set)
    for _, row in df.iterrows():
        disease = row['Disease']
        symptom = row['Symptom']
        if symptom and symptom != "nan":
            symptom_disease_map[symptom].add(disease)

    return symptom_disease_map

# Function to predict diseases based on symptoms
def predict_diseases(user_symptoms, symptom_disease_map):
    matching_diseases = set()
    for symptom in user_symptoms:
        symptom = symptom.strip().lower()
        if symptom in symptom_disease_map:
            matching_diseases.update(symptom_disease_map[symptom])
    return list(matching_diseases)

# Streamlit UI
def main():
    # Title
    st.markdown('<h1 style="color: #f0f8ff; text-align: center; font-size: 40px;">🩺 AI-Powered Medical Diagnosis System</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px; color: #d0e8f2;">Enter your symptoms to get possible disease predictions.</p>', unsafe_allow_html=True)

    # Load dataset
    symptom_disease_map = load_dataset()

    # User Input
    user_input = st.text_input("🔍 Enter symptoms (comma-separated)", "")

    # Predict button
    if st.button("Predict"):
        if user_input:
            user_symptoms = [symptom.strip() for symptom in user_input.split(',')]
            predicted_diseases = predict_diseases(user_symptoms, symptom_disease_map)

            if predicted_diseases:
                st.subheader("🩻 Possible Diseases:")
                for disease in predicted_diseases:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(to right, #a8e6cf, #dcedc1);
                            color: #064663;
                            padding: 15px;
                            border-radius: 10px;
                            margin-top: 10px;
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
                            font-size: 18px;
                            font-weight: bold;
                            text-align: center;">
                            ✅ {disease}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No matching disease found. Please check the symptoms entered.")
        else:
            st.warning("⚠️ Please enter at least one symptom.")

if __name__ == "__main__":
    main()
