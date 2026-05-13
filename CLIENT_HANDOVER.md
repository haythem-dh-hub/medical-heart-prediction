# 🏥 MediSpark AI: Deployment & Running Guide

This document provides step-by-step instructions for hospital administrators and technical clients to run the **MediSpark AI** Cardiovascular Risk Intelligence Platform.

---

## 🛠️ 1. Technical Prerequisites

Before running the application, ensure your machine has the following installed:

1.  **Python 3.12+**: [Download here](https://www.python.org/downloads/)
2.  **Java Runtime Environment (JRE) 8 or 11**: Required for Apache Spark's distributed processing.
3.  **Git & Git LFS**: Required to download the massive Parquet datasets correctly.

---

## 🚀 2. Installation Steps

Open your terminal (PowerShell or Command Prompt) and follow these steps:

### A. Clone and Prepare
```powershell
# Clone the repository
git clone <your-repository-url>
cd medical-heart-prediction

# Initialize Large File Storage to download the 2.1M records
git lfs pull
```

### B. Environment Setup
```powershell
# Create a dedicated virtual environment
python -m venv .venv

# Activate the environment
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install all medical and AI dependencies
pip install -r requirements.txt
```

---

## 🖥️ 3. Launching the Platform

To start the hospital dashboard and AI command center, run:

```powershell
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 🔍 4. Navigating the Platform

1.  **Dataset Explorer:** Start here to verify the **2,176,776 records** are correctly loaded from the archive.
2.  **Hospital Analytics:** View high-level heart risk trends across all 2M+ respondents.
3.  **Predict Patient Risk:** Enter specific patient vitals to receive an AI-powered cardiovascular risk score.
4.  **Big Data Processing:** View the real-time Apache Spark logs showing distributed cleaning and feature engineering.

---

## ❓ 5. Troubleshooting

*   **Java Errors:** If you see a "Java not found" error, ensure your `JAVA_HOME` environment variable is set to your Java installation folder.
*   **Missing Data:** If the row counts show 0, ensure you ran `git lfs pull` to download the actual Parquet files instead of the pointer files.
*   **Performance:** The first launch may take 10-20 seconds to initialize the Spark session for the 2M+ record analysis.

---
**Academic Context:** This platform is the primary deliverable for the Master's Thesis: *"Analyse de données médicales massives pour la prédiction des maladies cardiovasculaires à l’aide d’Apache Spark et des réseaux de neurones profonds."*
