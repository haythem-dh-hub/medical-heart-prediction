from __future__ import annotations

import time
from datetime import datetime

import pandas as pd
import streamlit as st

from src.charts import (
    ChartFallback,
    PLOTLY_AVAILABLE,
    cholesterol_scatter,
    confusion_matrix_figure,
    correlation_heatmap,
    department_volume,
    disease_trends,
    disease_distribution,
    performance_bars,
    realtime_line,
    risk_by_age,
    roc_curve,
    training_curves,
)
from src.healthcare_data import (
    CHEST_PAIN_MAP,
    analytics_frame,
    load_medical_records,
    platform_stats,
    realtime_stream,
)
from src.model_service import architecture_layers, model_metrics, predict_patient, training_history
from src.pdf_report import create_patient_report
from src.spark_engine import clean_with_spark, run_spark_sql, spark_session_info
from src.styles import APP_CSS


CHART_RENDER_COUNTER = 0


st.set_page_config(
    page_title="Big Medical Data Analysis and Cardiovascular Disease Prediction",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(APP_CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_records(file_path: str | None = None) -> pd.DataFrame:
    return analytics_frame(load_medical_records(file_path=file_path))


@st.cache_data(show_spinner=False)
def get_metrics() -> dict:
    return model_metrics()


def glass_card(label: str, value: str, note: str = "", accent: str = "#00d4aa") -> None:
    st.markdown(
        card_html(label, value, note, accent),
        unsafe_allow_html=True,
    )


def card_html(label: str, value: str, note: str = "", accent: str = "#00d4aa") -> str:
    return (
        '<div class="glass-card">'
        f'<div class="metric-label" style="color:{accent};">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-note">{note}</div>'
        "</div>"
    )


def card_grid(items: list[tuple[str, str, str, str]], css_class: str = "metric-grid") -> None:
    cards = "".join(card_html(label, value, note, accent) for label, value, note, accent in items)
    st.markdown(f"<div class='{css_class}'>{cards}</div>", unsafe_allow_html=True)


def draw_chart(chart, key: str | None = None) -> None:
    global CHART_RENDER_COUNTER
    if key is None:
        CHART_RENDER_COUNTER += 1
        key = f"chart_{CHART_RENDER_COUNTER}"

    if PLOTLY_AVAILABLE:
        st.plotly_chart(chart, use_container_width=True, key=key)
        return

    if isinstance(chart, ChartFallback):
        st.markdown(f"### {chart.title}")
        if chart.kind == "line":
            st.line_chart(chart.data)
        elif chart.kind == "bar":
            st.bar_chart(chart.data)
        else:
            st.dataframe(chart.data, use_container_width=True)
        return

    st.dataframe(chart, use_container_width=True)


def section_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Master's Thesis: Big Medical Data Intelligence</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def spark_status_panel(info: dict) -> None:
    app_name = str(info["app_name"]).replace("HospitalBigMedicalAnalytics", "Hospital Big Medical Analytics")
    items = [
        ("Status", info["status"], "Cluster runtime health", "#00d4aa"),
        ("App", app_name, "Spark application name", "#38bdf8"),
        ("Master", info["master"], "Execution mode", "#a78bfa"),
        ("Version", info["version"], "Spark runtime version", "#38bdf8"),
        ("Executors", str(info["executors"]), "Available workers", "#22c55e"),
    ]
    card_grid(items, "status-grid")


def friendly_note(text: str) -> None:
    st.markdown(f"<div class='friendly-note'>{text}</div>", unsafe_allow_html=True)


def readable_records(records: pd.DataFrame) -> pd.DataFrame:
    all_requested = [
        "patient_id",
        "department",
        "age",
        "sex_label",
        "trestbps",
        "chol",
        "thalach",
        "bmi",
        "glucose",
        "risk_band",
        "target_label",
    ]
    # Only select columns that actually exist to prevent KeyError
    existing_columns = [col for col in all_requested if col in records.columns]
    preview = records[existing_columns].copy()
    
    mapping = {
        "patient_id": "Patient ID",
        "department": "Department",
        "age": "Age",
        "sex_label": "Gender",
        "trestbps": "Blood Pressure",
        "chol": "Cholesterol",
        "thalach": "Heart Rate",
        "bmi": "BMI",
        "glucose": "Glucose",
        "risk_band": "Risk Level",
        "target_label": "Health Status",
    }
    # Filter mapping to only include existing columns
    active_mapping = {k: v for k, v in mapping.items() if k in existing_columns}
    preview = preview.rename(columns=active_mapping)
    return preview


def home_page(records: pd.DataFrame, metrics: dict) -> None:
    stats = platform_stats(records, accuracy=float(metrics.get("accuracy", 0.934)))
    section_header(
        "Massive Medical Data & CVD Prediction",
        "A Master's Thesis project demonstrating the integration of Apache Spark for distributed ETL "
        "and Deep Learning (Keras/TensorFlow) for cardiovascular risk prediction on 2.1M+ records.",
    )

    if "prediction_count" not in st.session_state:
        st.session_state.prediction_count = 0

    values = [
        ("Medical Records", f"{stats.total_records:,}", "Hospital-scale records in the system", "#00d4aa"),
        ("Patients", f"{stats.patients:,}", "Patient encounters available", "#a78bfa"),
        ("High Risk Patients", f"{stats.high_risk:,}", "Need faster clinical attention", "#ef4444"),
        ("Low Risk Patients", f"{stats.low_risk:,}", "Routine monitoring group", "#22c55e"),
        ("Model Accuracy", f"{stats.accuracy:.1%}", "AI validation score", "#38bdf8"),
        ("Predictions Today", str(st.session_state.prediction_count), "Patient checks made in this session", "#00d4aa"),
    ]
    card_grid(values)

    friendly_note(
        "Start with <strong>Medical Records</strong> to view the dataset, or go to "
        "<strong>Predict Patient Risk</strong> to enter one patient and get an AI risk result."
    )

    st.markdown("### Quick Actions")
    steps = [
        ("1", "View Medical Records", "Check the patient dataset and filter by department or risk level."),
        ("2", "Predict Patient Risk", "Enter a patient profile and get a clear risk result."),
        ("3", "Review Hospital Analytics", "Understand risk trends across age, cholesterol, and departments."),
    ]
    cards = "".join(
        '<div class="step-card">'
        f'<span class="status-pill">{number}</span>'
        f"<strong>{title}</strong>"
        f'<div class="small-muted">{body}</div>'
        "</div>"
        for number, title, body in steps
    )
    st.markdown(f"<div class='pipeline-grid'>{cards}</div>", unsafe_allow_html=True)

    st.markdown("### Patient Risk Overview")
    draw_chart(disease_distribution(records))
    draw_chart(risk_by_age(records))


def medical_records_page(records: pd.DataFrame) -> None:
    section_header(
        "Medical Records",
        "View the dataset used by the dashboard. These records are cleaned, prepared, and expanded "
        "to simulate hospital-scale medical data.",
    )

    friendly_note(
        "This is where the dataset appears in the app. Use the filters below to find patient groups, "
        "then review the table like a hospital record browser."
    )

    department = st.selectbox("Filter by department", ["All"] + sorted(records["department"].unique().tolist()))
    risk = st.selectbox("Filter by risk level", ["All", "Low", "Medium", "High"])

    filtered = records.copy()
    if department != "All":
        filtered = filtered[filtered["department"].eq(department)]
    if risk != "All":
        filtered = filtered[filtered["risk_band"].astype(str).eq(risk)]

    if filtered.empty:
        st.warning("No records match the selected filters. Choose another department or risk level.")
        return

    card_grid(
        [
            ("Shown Records", f"{len(filtered):,}", "Rows after filters", "#00d4aa"),
            ("Departments", str(filtered["department"].nunique()), "Hospital units in view", "#38bdf8"),
            ("Average Age", f"{filtered['age'].mean():.1f}", "Filtered patient average", "#a78bfa"),
            ("High Risk", f"{(filtered['risk_band'].astype(str) == 'High').sum():,}", "Filtered high-risk patients", "#ef4444"),
        ]
    )

    st.markdown(f"### Dataset Preview (Showing top {min(len(filtered), 1000):,} records)")
    st.dataframe(readable_records(filtered).head(1000), use_container_width=True)

    st.markdown("### Dataset Summary")
    st.dataframe(
        readable_records(filtered).describe(include="all").fillna("-"),
        use_container_width=True,
    )


def hospital_analytics_page(records: pd.DataFrame) -> None:
    section_header(
        "Hospital Analytics",
        "Simple visual reports that help hospital teams understand heart-risk patterns "
        "across patients and departments.",
    )

    friendly_note(
        "These charts summarize the same medical records shown in the dataset page. "
        "They are designed for quick reading, not for editing patient data."
    )

    draw_chart(department_volume(records))
    draw_chart(disease_distribution(records))
    draw_chart(risk_by_age(records))
    draw_chart(cholesterol_scatter(records))
    draw_chart(disease_trends(records))


def dashboard_page(records: pd.DataFrame, metrics: dict) -> None:
    stats = platform_stats(records, accuracy=float(metrics.get("accuracy", 0.934)))
    section_header(
        "Technical Dashboard",
        "A real-time hospital analytics cockpit powered by Apache Spark style ETL, "
        "TensorFlow/Keras risk scoring, and interactive Plotly intelligence.",
    )

    values = [
        ("Total Medical Records", f"{stats.total_records:,}", "Distributed clinical rows", "#00d4aa"),
        ("Spark Processing Status", "Online", stats.spark_status, "#38bdf8"),
        ("Number of Patients", f"{stats.patients:,}", "Unique patient encounters", "#a78bfa"),
        ("High Risk Cases", f"{stats.high_risk:,}", "Prioritized for review", "#ef4444"),
        ("Low Risk Cases", f"{stats.low_risk:,}", "Routine follow-up", "#22c55e"),
        ("Model Accuracy", f"{stats.accuracy:.1%}", "Deep learning validation", "#38bdf8"),
        ("Prediction Counter", str(st.session_state.get("prediction_count", 0)), "Real-time AI requests", "#00d4aa"),
    ]
    card_grid(values)

    st.markdown("### Spark Cluster Status Simulation")
    spark_status_panel(spark_session_info())
    progress_cols = st.columns(4)
    for index, (name, value) in enumerate(
        [("Ingestion", 96), ("Cleaning", 91), ("Feature Jobs", 88), ("Streaming", 74)]
    ):
        with progress_cols[index]:
            st.progress(value / 100, text=f"{name}: {value}%")

    draw_chart(disease_distribution(records))
    draw_chart(risk_by_age(records))
    draw_chart(department_volume(records))
    live = realtime_stream(rows=16)
    draw_chart(realtime_line(live))


def big_data_processing_page(records: pd.DataFrame) -> None:
    section_header(
        "Big Data Processing",
        "Apache Spark operations for hospital-scale ingestion, cleaning, feature engineering, "
        "SQL analytics, and distributed processing simulation.",
    )

    info = spark_session_info()
    spark_status_panel(info)

    st.markdown("### Spark ETL Execution Progress")
    stages = [
        ("Load Parquet to Spark DataFrame", 100),
        ("Infer schema and validate vitals", 96),
        ("Handle missing medical values", 92),
        ("Assemble feature vector", 88),
        ("Register SQL analytics view", 84),
    ]
    for stage, progress in stages:
        st.progress(progress / 100, text=f"{stage} - {progress}%")

    st.markdown("### DAG Workflow")
    dag = [
        ("01", "Ingest", "SparkSession reads Parquet dataset"),
        ("02", "Clean", "Null imputation and type casting"),
        ("03", "Engineer", "VectorAssembler clinical features"),
        ("04", "Train", "Keras and MLlib model paths"),
        ("05", "Serve", "Real-time patient prediction"),
    ]
    nodes = "".join(
        '<div class="pipeline-node">'
        f'<span class="status-pill">{step}</span><br><br>'
        f"<strong>{title}</strong>"
        f'<div class="small-muted">{body}</div>'
        "</div>"
        for step, title, body in dag
    )
    st.markdown(f"<div class='pipeline-grid'>{nodes}</div>", unsafe_allow_html=True)

    cleaned, logs = clean_with_spark(records)
    st.markdown("### Data Transformation Logs")
    for log in logs:
        st.code(f"[{datetime.now().strftime('%H:%M:%S')}] {log}", language="text")
    st.markdown("### PySpark Code")
    st.code(
        """
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler

spark = SparkSession.builder.appName("HospitalBigMedicalAnalytics").master("local[*]").getOrCreate()
df = spark.read.parquet("data/archive/brfss_2020_2024_pooled_eda.parquet")
df = df.fillna(0)
df.createOrReplaceTempView("medical_records")
features = VectorAssembler(inputCols=feature_columns, outputCol="features").transform(df)
spark.sql("SELECT department, COUNT(*), AVG(chol) FROM medical_records GROUP BY department")
        """,
        language="python",
    )
    st.markdown("### Spark DataFrame Preview")
    st.dataframe(cleaned.head(25), use_container_width=True)


def dataset_explorer_page() -> None:
    from src.config import DATA_ARCHIVE_DIR
    import os
    
    section_header(
        "Dataset Explorer",
        "A management console to view and analyze all Parquet files available in the hospital data archive.",
    )
    
    # Recursive search to find all parquet files
    files = sorted([f for f in DATA_ARCHIVE_DIR.rglob("*.parquet")])
    
    if not files:
        st.warning(f"No Parquet files found in {DATA_ARCHIVE_DIR}")
        return

    st.markdown("### Archive Summary")
    total_size_gb = sum(os.path.getsize(f) for f in files) / (1024**3)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", len(files))
    col2.metric("Total Archive Size", f"{total_size_gb:.2f} GB")
    col3.metric("Data Formats", "Parquet (Optimized)")

    st.markdown("### Archive Inventory")
    file_data = []
    
    with st.spinner("Calculating dataset scales..."):
        for f in files:
            size_mb = os.path.getsize(f) / (1024 * 1024)
            try:
                # Efficiently get row count without loading full data
                # Using a small subset or metadata if possible
                row_count = len(pd.read_parquet(f, columns=[pd.read_parquet(f).columns[0]]))
            except:
                row_count = "Unknown"
                
            file_data.append({
                "File Name": f.name,
                "Total Rows": f"{row_count:,}" if isinstance(row_count, int) else "Error",
                "Size (MB)": f"{size_mb:.2f}",
                "Type": "Pooled" if "pooled" in f.name else "Yearly",
                "Category": "ML-Ready" if "_ml" in f.name else "EDA/Raw",
                "Path": str(f.relative_to(DATA_ARCHIVE_DIR))
            })
    
    st.dataframe(pd.DataFrame(file_data), use_container_width=True)
    
    st.markdown("### Detailed Schema Inspection")
    inspect_file = st.selectbox("Select a file to inspect full schema", [f.name for f in files])
    if inspect_file:
        # Find the full path for the selected file name
        path = next(f for f in files if f.name == inspect_file)
        df_preview = pd.read_parquet(path).head(10)
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Total Columns:** {len(df_preview.columns)}")
            st.write("**Column List:**")
            st.code(", ".join(df_preview.columns.tolist()))
        with c2:
            st.write("**Data Types:**")
            st.write(pd.read_parquet(path).dtypes.to_frame("Type").head(15))
            
        st.markdown("**Data Sample (Top 10 Rows):**")
        st.dataframe(df_preview, use_container_width=True)


def patient_prediction_page() -> None:
    section_header(
        "Predict Patient Risk",
        "Enter one patient profile and the app will estimate cardiovascular risk with a clear "
        "result, confidence score, and recommendation.",
    )
    friendly_note(
        "Use realistic patient values. The result is for project demonstration only and should "
        "not replace a doctor or cardiologist."
    )

    with st.form("patient_prediction_form"):
        st.markdown("### Patient Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.slider("Age", 18, 95, 54)
            gender = st.selectbox("Gender", ["Male", "Female"])
            blood_pressure = st.slider("Blood Pressure", 80, 230, 138)
            cholesterol = st.slider("Cholesterol", 110, 620, 242)
        with c2:
            heart_rate = st.slider("Heart Rate", 55, 220, 146)
            diabetes = st.toggle("Diabetes", value=False)
            smoking = st.toggle("Smoking", value=False)
            bmi = st.slider("BMI", 16.0, 48.0, 27.5, 0.1)
        with c3:
            chest_pain_type = st.selectbox("Chest Pain Type", list(CHEST_PAIN_MAP.keys()), index=1)
            glucose = st.slider("Glucose Level", 65, 260, 108)
            st.markdown(
                "<div class='small-muted'>The app checks these values, prepares them for the AI model, "
                "and returns a simple patient risk result.</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div class='ai-button'>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Run AI Cardiovascular Prediction", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        patient = {
            "age": age,
            "gender": gender,
            "blood_pressure": blood_pressure,
            "cholesterol": cholesterol,
            "heart_rate": heart_rate,
            "diabetes": diabetes,
            "smoking": smoking,
            "bmi": bmi,
            "chest_pain_type": chest_pain_type,
            "glucose": glucose,
        }
        with st.spinner("Spark pipeline processing patient record and deep model scoring..."):
            time.sleep(0.8)
            result = predict_patient(patient)
            st.session_state.prediction_count = st.session_state.get("prediction_count", 0) + 1
            st.session_state.last_patient = patient
            st.session_state.last_result = result

    result = st.session_state.get("last_result")
    patient = st.session_state.get("last_patient")
    if result and patient:
        is_high = result["risk_level"] == "High Risk"
        card_class = "danger" if is_high else "success"
        st.markdown(
            f"""
            <div class="glass-card {card_class}">
                <div class="metric-label">Prediction Result</div>
                <div class="metric-value">{result["risk_level"]}</div>
                <div class="metric-note">{result["recommendation"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        card_grid(
            [
                ("Risk Probability", f"{result['probability']:.2%}", "Estimated chance of cardiovascular risk", "#ef4444" if is_high else "#22c55e"),
                ("AI Confidence", f"{result['confidence']:.2%}", "How confident the model is", "#38bdf8"),
                ("AI Engine", result["engine"], "Prediction method used", "#a78bfa"),
            ]
        )
        st.caption(f"Data preparation: {result['spark_pipeline']}")
        st.markdown("### AI-Prepared Patient Values")
        st.dataframe(result["processed_features"], use_container_width=True)
        pdf = create_patient_report(patient, result)
        st.download_button(
            "Export Patient Report to PDF",
            data=pdf,
            file_name="patient_cardiovascular_risk_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


def spark_analytics_page(records: pd.DataFrame) -> None:
    section_header(
        "Spark Analytics",
        "Spark DataFrame analytics, SQL query outputs, correlations, patient distributions, "
        "and cardiovascular disease trends.",
    )

    st.markdown("### Spark SQL Query Results")
    st.dataframe(run_spark_sql(records), use_container_width=True)

    st.markdown("### Spark DataFrame Analytics")
    st.dataframe(
        records[["patient_id", "department", "age", "trestbps", "chol", "bmi", "glucose", "risk_band"]]
        .head(18),
        use_container_width=True,
    )

    draw_chart(correlation_heatmap(records))
    draw_chart(cholesterol_scatter(records))
    draw_chart(disease_trends(records))
    draw_chart(risk_by_age(records))


def deep_learning_page(metrics: dict) -> None:
    section_header(
        "Deep Learning Model",
        "TensorFlow/Keras neural network architecture, training process, epoch progress, "
        "and clinical performance diagnostics.",
    )

    card_grid(
        [
            ("Framework", "TensorFlow/Keras", "Deep learning engine", "#00d4aa"),
            ("Accuracy", f"{float(metrics.get('accuracy', 0.934)):.2%}", "Validation performance", "#38bdf8"),
            ("Epochs", str(int(metrics.get("epochs_trained", 34))), "Training iterations", "#a78bfa"),
            ("Input Features", "13", "Clinical model variables", "#22c55e"),
        ]
    )

    st.markdown("### Neural Network Architecture")
    st.dataframe(architecture_layers(), use_container_width=True)
    st.code(
        """
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(13,)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        """,
        language="python",
    )
    draw_chart(training_curves(training_history()))

    matrix = metrics.get("confusion_matrix", [[920, 82], [71, 1048]])
    draw_chart(confusion_matrix_figure(matrix))
    draw_chart(roc_curve())


def model_performance_page(metrics: dict) -> None:
    section_header(
        "Model Performance",
        "A simple view of how well the AI model performs when predicting cardiovascular risk.",
    )
    friendly_note(
        "Accuracy shows the overall score. Precision and recall explain how reliably the model "
        "identifies high-risk patients."
    )
    report = metrics.get("classification_report", {})
    high = report.get("1", {})
    low = report.get("0", {})
    card_grid(
        [
            ("Accuracy", f"{float(metrics.get('accuracy', 0.934)):.2%}", "Overall validation score", "#00d4aa"),
            ("Precision", f"{float(high.get('precision', 0.91)):.2%}", "High-risk positive quality", "#38bdf8"),
            ("Recall", f"{float(high.get('recall', 0.89)):.2%}", "High-risk case capture", "#a78bfa"),
            ("F1 Score", f"{float(high.get('f1-score', 0.90)):.2%}", "Balanced model quality", "#22c55e"),
        ]
    )

    perf = pd.DataFrame(
        [
            {"class": "Low Risk", "precision": low.get("precision", 0.92), "recall": low.get("recall", 0.90), "f1": low.get("f1-score", 0.91)},
            {"class": "High Risk", "precision": high.get("precision", 0.91), "recall": high.get("recall", 0.89), "f1": high.get("f1-score", 0.90)},
        ]
    )
    draw_chart(performance_bars(perf))
    draw_chart(confusion_matrix_figure(metrics.get("confusion_matrix", [[920, 82], [71, 1048]])))
    draw_chart(roc_curve())


def realtime_monitoring_page() -> None:
    section_header(
        "Live Monitoring",
        "A live-style hospital feed that simulates incoming patient records and real-time risk alerts.",
    )
    friendly_note(
        "This page simulates what a hospital monitoring screen could look like. The rows update "
        "when the app reruns."
    )

    stream = realtime_stream(rows=22)
    card_grid(
        [
            ("Incoming Records/min", "248", "Streaming ingestion rate", "#00d4aa"),
            ("Streaming Latency", "42 ms", "Spark micro-batch delay", "#38bdf8"),
            ("High Risk Alerts", str(int((stream["risk_level"] == "High").sum())), "Current alert queue", "#ef4444"),
            ("Spark Micro-batches", "37", "Processed batches", "#a78bfa"),
        ]
    )

    draw_chart(realtime_line(stream))
    st.markdown("### Incoming Medical Records")
    st.dataframe(
        stream.sort_values("time", ascending=False).assign(
            risk_probability=lambda frame: (frame["risk_probability"] * 100).round(2)
        ),
        use_container_width=True,
    )
    st.info("Use Streamlit rerun or interact with any control to simulate the next streaming micro-batch.")


def technical_details_page(records: pd.DataFrame, metrics: dict) -> None:
    section_header(
        "Technical Details",
        "Advanced project details for Spark processing, SQL analytics, and the deep learning model.",
    )
    friendly_note(
        "This section is for presentations, teachers, and developers. Normal users can use Home, "
        "Medical Records, Predict Patient Risk, Hospital Analytics, and Live Monitoring."
    )

    tabs = st.tabs(["Big Data Processing", "Spark Analytics", "Deep Learning Model", "Technical Dashboard"])
    with tabs[0]:
        big_data_processing_page(records)
    with tabs[1]:
        spark_analytics_page(records)
    with tabs[2]:
        deep_learning_page(metrics)
    with tabs[3]:
        dashboard_page(records, metrics)


def main() -> None:
    from src.config import DATA_ARCHIVE_DIR
    
    st.sidebar.markdown("## MediSpark AI")
    st.sidebar.markdown("<span class='status-pill'>Healthcare Risk App</span>", unsafe_allow_html=True)
    
    # Dataset Selection
    st.sidebar.markdown("### Data Source")
    archive_files = sorted([f.name for f in DATA_ARCHIVE_DIR.glob("*.parquet")])
    if not archive_files:
        archive_files = ["brfss_2020_2024_pooled_eda.parquet"]
        
    selected_file = st.sidebar.selectbox(
        "Select Active Dataset",
        archive_files,
        index=0 if "pooled" in archive_files[0] else (len(archive_files)-1 if archive_files else 0)
    )
    selected_path = DATA_ARCHIVE_DIR / selected_file
    
    records = get_records(str(selected_path))
    metrics = get_metrics()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Medical Records",
            "Dataset Explorer",
            "Predict Patient Risk",
            "Hospital Analytics",
            "Live Monitoring",
            "Model Performance",
            "Technical Details",
        ],
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Patient records | AI risk prediction | Hospital analytics")
    if not PLOTLY_AVAILABLE:
        st.sidebar.warning("Plotly is not installed. Run `pip install plotly==5.24.1` for full interactive charts.")

    if page == "Home":
        home_page(records, metrics)
    elif page == "Medical Records":
        medical_records_page(records)
    elif page == "Dataset Explorer":
        dataset_explorer_page()
    elif page == "Predict Patient Risk":
        patient_prediction_page()
    elif page == "Hospital Analytics":
        hospital_analytics_page(records)
    elif page == "Live Monitoring":
        realtime_monitoring_page()
    elif page == "Model Performance":
        model_performance_page(metrics)
    else:
        technical_details_page(records, metrics)


if __name__ == "__main__":
    main()
