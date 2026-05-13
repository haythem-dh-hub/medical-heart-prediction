# MediSpark AI: Massive Medical Data Analysis & CVD Prediction

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5.3-orange.svg)](https://spark.apache.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.18.0-red.svg)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40.2-FF4B4B.svg)](https://streamlit.io/)

A professional healthcare analytics platform developed for a Master's Thesis. This project demonstrates distributed ETL pipelines using **Apache Spark** and cardiovascular risk prediction using **Deep Learning** (Neural Networks) on a massive dataset of **2.1M+ medical records**.

---

## 🔬 Core Objectives
- **Big Data Processing:** Distributed ingestion and cleaning of 2.1 million BRFSS records using Spark SQL and DataFrames.
- **Deep Learning Intelligence:** High-accuracy cardiovascular risk classification via a multi-layer Keras/TensorFlow neural network.
- **Hospital Intelligence:** A real-time command center for clinical risk monitoring and patient-level reporting.

## 📂 Project Structure
```text
medical-heart-prediction/
├── app.py              # Main Streamlit Dashboard
├── src/                # Modular Source Code
│   ├── spark_engine.py # Spark Session & Distributed ETL
│   ├── deep_learning.py# Neural Network Architecture
│   ├── healthcare_data.py# Massive Data Handling Logic
│   └── ...
├── data/
│   ├── archive/        # 2M+ Record Parquet Files (See Data section)
│   └── raw/            # Seed CSV samples
├── models/             # Pre-trained Keras artifacts & Scalers
└── docs/               # Project Plan & Thesis Documentation
```

## 🚀 Installation & Setup

### 1. Prerequisites
- **Python 3.12+**
- **Java 8 or 11** (Required for Apache Spark)
- **Apache Spark 3.5.x**

### 2. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/your-username/medical-heart-prediction.git
cd medical-heart-prediction

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Platform
```powershell
streamlit run app.py
```

## 📊 Dataset Information
This project utilizes the **CDC BRFSS (Behavioral Risk Factor Surveillance System)** multi-year pooled dataset (2020-2024), containing over **2.17 million respondents**.
> **Note:** Due to size constraints, the `.parquet` files in `data/archive/` are managed via Git LFS or should be downloaded separately as per the instructions in `data/README.md`.

## 📜 Academic Realignment
This project is part of a Master's Thesis titled:
> *"Analyse de données médicales massives pour la prédiction des maladies cardiovasculaires à l’aide d’Apache Spark et des réseaux de neurones profonds"*

---
**Disclaimer:** This is a research project and is not intended for clinical use as a medical device.
