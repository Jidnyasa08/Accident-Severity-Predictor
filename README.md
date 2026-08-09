# Accident Severity Predictor & Risk Analytics System

A machine-learning-based web application and analytics dashboard designed to predict road accident severity risk and provide interactive insights into high-risk hotspots, temporal trends, and key contributing features.

---

## 📌 Project Overview

Traffic accident severity prediction is crucial for emergency dispatch prioritization, urban traffic safety planning, and risk mitigation. This system leverages historical accident records to:
1. **Predict Real-Time Accident Severity**: Classifies potential accidents into `Slight Injury`, `Serious Injury`, or `Fatal Injury` with normalized confidence probability distributions.
2. **Identify High-Risk Hotspots**: Evaluates area-based incident density and weighted risk scores.
3. **Analyze Temporal Trends**: Tracks accident volumes across 24-hour cycles and morning/afternoon/evening/night time windows.
4. **Explain Model Decisions**: Visualizes Gini importance scores for the underlying Random Forest model.

---

## 🛠️ Technology Stack

- **Frontend & Web Framework**: [Streamlit](https://streamlit.io/)
- **Machine Learning**: `scikit-learn`, `RandomForestClassifier`
- **Data Preprocessing & Encoding**: `pandas`, `numpy`, `joblib` (`LabelEncoder`)
- **Data Visualizations**: `plotly.express`, `plotly.graph_objects`
- **Language**: Python 3.10+

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.10+ and pip are installed on your system.

### 2. Install Required Dependencies
Run the following command in your terminal:
```bash
pip install streamlit pandas numpy scikit-learn joblib plotly
```

### 3. Run the Streamlit Application
Navigate to the project root directory and run:
```bash
streamlit run app/app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## 📂 Repository Structure

```
Project_1_Accident_Severity_Predictor/
├── app/
│   ├── app.py                      # Main Streamlit web application & analytics dashboard
├── Dataset/
│   ├── Road.csv                    # Original raw accident dataset (12,316 records × 32 columns)
│   ├── encoded_road.csv            # Preprocessed & encoded dataset dump
│   ├── X_prepared.csv              # Input feature matrix
│   └── Y_prepared.csv              # Target severity labels
├── Images/                         # Visual assets & generated plots
├── Model/
│   ├── accident_severity_model.pkl # Trained Random Forest Classifier model artifact
│   └── encoders.pkl                # Dictionary of fitted Scikit-Learn LabelEncoders
├── Notebook/                       # Step-by-step exploratory notebooks (EDA, Cleaning, Model Training)
├── Presentation/                   # Presentation slides & demo materials
├── Python_Code/                    # Standalone Python scripts & helper modules
├── Report/                         # Exported analysis CSVs, feature importance & metrics summary reports
├── .python-version                 # Python version specification (3.13.5)
├── README.md                       # Main repository documentation
└── requirements.txt                # Python dependencies manifest
```

---

## 🔮 Application Features & Navigation

- **🔮 Severity Predictor**: Interactive input form covering 31 input variables (Driver Demographics, Vehicle Characteristics, Environmental Factors, Road Geometry, and Collision Details).
- **📊 Accident Overview**: High-level distribution of accident severity levels and weather interactions.
- **📍 Area Risk & Hotspots**: Area-based accident frequencies and calculated **Weighted Risk Scores** ($\text{Fatal}\times 3 + \text{Serious}\times 2 + \text{Slight}\times 1$).
- **🕒 Time-of-Day Analysis**: 24-hour hourly trend line charts and severity heatmaps across morning, afternoon, evening, and night time windows.
- **🧠 Model Insights & XAI**: Feature importance analysis displaying the top 10 factors influencing model decisions.

---

## 📊 Machine Learning Model Architecture

- **Algorithm**: `RandomForestClassifier` (Ensemble of Decision Trees)
- **Input Features**: 31 variables (29 categorical label-encoded, 2 numerical)
- **Target Variable**: `Accident_severity`
  - `0`: Fatal Injury
  - `1`: Serious Injury
  - `2`: Slight Injury
- **Performance**: ~84.1% Classification Accuracy
