# from __future__ import annotations

# import time
# import os
# from datetime import datetime

# import pandas as pd
# import streamlit as st

# from src.charts import (
#     ChartFallback,
#     PLOTLY_AVAILABLE,
#     cholesterol_scatter,
#     confusion_matrix_figure,
#     correlation_heatmap,
#     department_volume,
#     disease_trends,
#     disease_distribution,
#     performance_bars,
#     realtime_line,
#     risk_by_age,
#     roc_curve,
#     training_curves,
# )
# from src.healthcare_data import (
#     CHEST_PAIN_MAP,
#     analytics_frame,
#     load_medical_records,
#     platform_stats,
#     realtime_stream,
# )
# from src.model_service import architecture_layers, model_metrics, predict_patient, training_history
# from src.pdf_report import create_patient_report
# from src.spark_engine import clean_with_spark, run_spark_sql, spark_session_info
# from src.i18n import TRANSLATIONS
# from src.styles import APP_CSS


# CHART_RENDER_COUNTER = 0


# st.set_page_config(
#     page_title="Big Medical Data Analysis and Cardiovascular Disease Prediction",
#     page_icon="AI",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# st.markdown(APP_CSS, unsafe_allow_html=True)

# # Initialize session state for language
# if "language" not in st.session_state:
#     st.session_state.language = "English"

# t = TRANSLATIONS[st.session_state.language]
# is_rtl = st.session_state.language == "Arabic"


# @st.cache_data(show_spinner=False)
# def get_records(file_path: str | None = None) -> pd.DataFrame:
#     return analytics_frame(load_medical_records(file_path=file_path))


# @st.cache_data(show_spinner=False)
# def get_metrics() -> dict:
#     return model_metrics()


# def glass_card(label: str, value: str, note: str = "", accent: str = "#00d4aa") -> None:
#     st.markdown(
#         card_html(label, value, note, accent),
#         unsafe_allow_html=True,
#     )


# def card_html(label: str, value: str, note: str = "", accent: str = "#00d4aa") -> str:
#     return (
#         '<div class="glass-card">'
#         f'<div class="metric-label" style="color:{accent};">{label}</div>'
#         f'<div class="metric-value">{value}</div>'
#         f'<div class="metric-note">{note}</div>'
#         "</div>"
#     )


# def card_grid(items: list[tuple[str, str, str, str]], css_class: str = "metric-grid") -> None:
#     cards = "".join(card_html(label, value, note, accent) for label, value, note, accent in items)
#     st.markdown(f"<div class='{css_class}'>{cards}</div>", unsafe_allow_html=True)


# def draw_chart(chart, key: str | None = None) -> None:
#     global CHART_RENDER_COUNTER
#     if key is None:
#         CHART_RENDER_COUNTER += 1
#         key = f"chart_{CHART_RENDER_COUNTER}"

#     if PLOTLY_AVAILABLE:
#         st.plotly_chart(chart, use_container_width=True, key=key)
#         return

#     if isinstance(chart, ChartFallback):
#         st.markdown(f"### {chart.title}")
#         if chart.kind == "line":
#             st.line_chart(chart.data)
#         elif chart.kind == "bar":
#             st.bar_chart(chart.data)
#         else:
#             st.dataframe(chart.data, use_container_width=True)
#         return

#     st.dataframe(chart, use_container_width=True)


# def section_header(title: str, subtitle: str) -> None:
#     st.markdown(
#         f"""
#         <div class="hero">
#             <div class="eyebrow">{t['eyebrow']}</div>
#             <h1>{title}</h1>
#             <p>{subtitle}</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# def spark_status_panel(info: dict) -> None:
#     app_name = str(info["app_name"]).replace("HospitalBigMedicalAnalytics", "Hospital Big Medical Analytics")
#     items = [
#         (t["status"], info["status"], "Cluster runtime health", "#00d4aa"),
#         (t["app"], app_name, "Spark application name", "#38bdf8"),
#         (t["master"], info["master"], "Execution mode", "#a78bfa"),
#         (t["version"], info["version"], "Spark runtime version", "#38bdf8"),
#         (t["executors"], str(info["executors"]), "Available workers", "#22c55e"),
#     ]
#     card_grid(items, "status-grid")


# def friendly_note(text: str) -> None:
#     st.markdown(f"<div class='friendly-note'>{text}</div>", unsafe_allow_html=True)


# def readable_records(records: pd.DataFrame) -> pd.DataFrame:
#     all_requested = [
#         "patient_id",
#         "department",
#         "age",
#         "sex_label",
#         "trestbps",
#         "chol",
#         "thalach",
#         "bmi",
#         "glucose",
#         "risk_band",
#         "target_label",
#     ]
#     existing_columns = [col for col in all_requested if col in records.columns]
#     preview = records[existing_columns].copy()
    
#     mapping = {
#         "patient_id": "Patient ID",
#         "department": "Department",
#         "age": "Age",
#         "sex_label": "Gender",
#         "trestbps": "Blood Pressure",
#         "chol": "Cholesterol",
#         "thalach": "Heart Rate",
#         "bmi": "BMI",
#         "glucose": "Glucose",
#         "risk_band": "Risk Level",
#         "target_label": "Health Status",
#     }
#     active_mapping = {k: v for k, v in mapping.items() if k in existing_columns}
#     preview = preview.rename(columns=active_mapping)
#     return preview


# def home_page(records: pd.DataFrame, metrics: dict) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     stats = platform_stats(records, accuracy=float(metrics.get("accuracy", 0.934)))
#     section_header(t["title"], t["subtitle"])

#     if "prediction_count" not in st.session_state:
#         st.session_state.prediction_count = 0

#     values = [
#         (t["records"], f"{stats.total_records:,}", t["records_desc"][:35] + "...", "#00d4aa"),
#         (t["patients"], f"{stats.patients:,}", t["unique_patients"], "#a78bfa"),
#         (t["high_risk"], f"{stats.high_risk:,}", t["critical_queue"], "#ef4444"),
#         (t["filter_risk"], f"{stats.low_risk:,}", t["routine_monitoring"], "#22c55e"),
#         (t["accuracy"], f"{stats.accuracy:.1%}", t["deep_score"], "#38bdf8"),
#         (t["today"], str(st.session_state.prediction_count), t["session_preds"], "#00d4aa"),
#     ]
#     card_grid(values)
#     friendly_note(t["friendly_home"])

#     st.markdown(f"### {t['quick_actions']}")
#     steps = [
#         ("📋", t["action_records_title"], t["action_records_body"]),
#         ("🧠", t["action_predict_title"], t["action_predict_body"]),
#         ("📊", t["action_analytics_title"], t["action_analytics_body"]),
#     ]
#     cards = "".join(
#         '<div class="step-card">'
#         f'<span class="status-pill">{number}</span>'
#         f"<strong>{title}</strong>"
#         f'<div class="small-muted">{body}</div>'
#         "</div>"
#         for number, title, body in steps
#     )
#     st.markdown(f"<div class='pipeline-grid'>{cards}</div>", unsafe_allow_html=True)

#     st.markdown(f"### {t['risk_overview']}")
#     draw_chart(disease_distribution(records))
#     draw_chart(risk_by_age(records))
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def medical_records_page(records: pd.DataFrame) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["records"], t["records_desc"])
#     friendly_note(t["records_friendly"])

#     c1, c2 = st.columns(2)
#     with c1:
#         department = st.selectbox(t["filter_dept"], [t["filter_all"]] + sorted(records["department"].unique().tolist()))
#     with c2:
#         risk = st.selectbox(t["filter_risk"], [t["filter_all"], "Low", "Medium", "High"])

#     filtered = records.copy()
#     if department != t["filter_all"]:
#         filtered = filtered[filtered["department"].eq(department)]
#     if risk != t["filter_all"]:
#         filtered = filtered[filtered["risk_band"].astype(str).eq(risk)]

#     if filtered.empty:
#         st.warning(t["no_match"])
#         if is_rtl: st.markdown("</div>", unsafe_allow_html=True)
#         return

#     card_grid([
#         (t["shown"], f"{len(filtered):,}", "", "#00d4aa"),
#         (t["hospital_units"], str(filtered["department"].nunique()), "", "#38bdf8"),
#         (t["avg"], f"{filtered['age'].mean():.1f}", "", "#a78bfa"),
#         (t["high_risk"], f"{(filtered['risk_band'].astype(str) == 'High').sum():,}", "", "#ef4444"),
#     ])

#     st.markdown(f"### {t['dataset_preview']} (Showing top {min(len(filtered), 1000):,} records)")
#     st.info(t["preview_limit_note"])
#     st.dataframe(readable_records(filtered).head(1000), use_container_width=True)

#     st.markdown(f"### {t['dataset_summary']}")
#     st.dataframe(readable_records(filtered).describe(include="all").fillna("-"), use_container_width=True)
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def hospital_analytics_page(records: pd.DataFrame) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["analytics"], t["analytics_desc"])
#     friendly_note(t["analytics_friendly"])

#     draw_chart(department_volume(records))
#     draw_chart(disease_distribution(records))
#     draw_chart(risk_by_age(records))
#     draw_chart(cholesterol_scatter(records))
#     draw_chart(disease_trends(records))
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def dashboard_page(records: pd.DataFrame, metrics: dict) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     stats = platform_stats(records, accuracy=float(metrics.get("accuracy", 0.934)))
#     section_header(t["technical_dashboard"], t["technical_desc"])

#     values = [
#         (t["total_records"], f"{stats.total_records:,}", "Distributed clinical rows", "#00d4aa"),
#         (t["spark_status"], "Online", stats.spark_status, "#38bdf8"),
#         (t["patients"], f"{stats.patients:,}", "Unique patient encounters", "#a78bfa"),
#         (t["high_risk"], f"{stats.high_risk:,}", "Prioritized for review", "#ef4444"),
#         (t["filter_risk"], f"{stats.low_risk:,}", "Routine follow-up", "#22c55e"),
#         (t["accuracy"], f"{stats.accuracy:.1%}", "Deep learning validation", "#38bdf8"),
#         ("Prediction Counter", str(st.session_state.get("prediction_count", 0)), "Real-time AI requests", "#00d4aa"),
#     ]
#     card_grid(values)

#     st.markdown("### Spark Cluster Status Simulation")
#     spark_status_panel(spark_session_info())
#     progress_cols = st.columns(4)
#     for index, (name, value) in enumerate(
#         [("Ingestion", 96), ("Cleaning", 91), ("Feature Jobs", 88), ("Streaming", 74)]
#     ):
#         with progress_cols[index]:
#             st.progress(value / 100, text=f"{name}: {value}%")

#     draw_chart(disease_distribution(records))
#     draw_chart(risk_by_age(records))
#     draw_chart(department_volume(records))
#     live = realtime_stream(rows=16)
#     draw_chart(realtime_line(live))
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def big_data_processing_page(records: pd.DataFrame) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["big_data_processing"], t["technical_desc"])

#     info = spark_session_info()
#     spark_status_panel(info)

#     st.markdown("### Spark ETL Execution Progress")
#     stages = [
#         ("Load Parquet to Spark DataFrame", 100),
#         ("Infer schema and validate vitals", 96),
#         ("Handle missing medical values", 92),
#         ("Assemble feature vector", 88),
#         ("Register SQL analytics view", 84),
#     ]
#     for stage, progress in stages:
#         st.progress(progress / 100, text=f"{stage} - {progress}%")

#     st.markdown("### DAG Workflow")
#     dag = [
#         ("01", "Ingest", "SparkSession reads Parquet dataset"),
#         ("02", "Clean", "Null imputation and type casting"),
#         ("03", "Engineer", "VectorAssembler clinical features"),
#         ("04", "Train", "Keras and MLlib model paths"),
#         ("05", "Serve", "Real-time patient prediction"),
#     ]
#     nodes = "".join(
#         '<div class="pipeline-node">'
#         f'<span class="status-pill">{step}</span><br><br>'
#         f"<strong>{title}</strong>"
#         f'<div class="small-muted">{body}</div>'
#         "</div>"
#         for step, title, body in dag
#     )
#     st.markdown(f"<div class='pipeline-grid'>{nodes}</div>", unsafe_allow_html=True)

#     cleaned, logs = clean_with_spark(records)
#     st.markdown("### Data Transformation Logs")
#     for log in logs:
#         st.code(f"[{datetime.now().strftime('%H:%M:%S')}] {log}", language="text")
    
#     st.markdown("### PySpark Code")
#     st.code(
#         """
# from pyspark.sql import SparkSession
# from pyspark.ml.feature import VectorAssembler

# spark = SparkSession.builder.appName("HospitalBigMedicalAnalytics").master("local[*]").getOrCreate()
# df = spark.read.parquet("data/archive/brfss_2020_2024_pooled_eda.parquet")
# df = df.fillna(0)
# df.createOrReplaceTempView("medical_records")
# features = VectorAssembler(inputCols=feature_columns, outputCol="features").transform(df)
# spark.sql("SELECT department, COUNT(*), AVG(chol) FROM medical_records GROUP BY department")
#         """,
#         language="python",
#     )
#     st.markdown("### Spark DataFrame Preview")
#     st.dataframe(cleaned.head(25), use_container_width=True)
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def dataset_explorer_page() -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     from src.config import DATA_ARCHIVE_DIR
#     import os
    
#     section_header(t["explorer"], "A management console to view and analyze all Parquet files available in the hospital data archive.")
    
#     files = sorted([f for f in DATA_ARCHIVE_DIR.rglob("*.parquet")])
#     if not files:
#         st.warning(f"No Parquet files found in {DATA_ARCHIVE_DIR}")
#         if is_rtl: st.markdown("</div>", unsafe_allow_html=True)
#         return

#     st.markdown("### Archive Summary")
#     total_size_gb = sum(os.path.getsize(f) for f in files) / (1024**3)
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Total Files", len(files))
#     c2.metric("Total Archive Size", f"{total_size_gb:.2f} GB")
#     c3.metric("Data Formats", "Parquet (Optimized)")

#     st.markdown("### Archive Inventory")
#     file_data = []
#     with st.spinner("Calculating scales..."):
#         for f in files:
#             size_mb = os.path.getsize(f) / (1024 * 1024)
#             try:
#                 row_count = len(pd.read_parquet(f, columns=[pd.read_parquet(f).columns[0]]))
#             except:
#                 row_count = "Unknown"
#             file_data.append({
#                 "File": f"📄 {f.name}",
#                 "Records": row_count,
#                 "Size (MB)": round(size_mb, 2),
#                 "Source": "Multi-Year" if "pooled" in f.name else "Yearly",
#                 "Format": "ML-Ready" if "_ml" in f.name else "Raw Data"
#             })
    
#     st.dataframe(pd.DataFrame(file_data), use_container_width=True, hide_index=True)
    
#     st.markdown(f"### {t['explorer']} - Detailed Schema Inspection")
#     inspect_file = st.selectbox("Select file", [f.name for f in files])
#     if inspect_file:
#         path = next(f for f in files if f.name == inspect_file)
#         df_p = pd.read_parquet(path).head(10)
#         c1, c2 = st.columns(2)
#         with c1:
#             st.write(f"**Total Columns:** {len(df_p.columns)}")
#             st.code(", ".join(df_p.columns.tolist()))
#         with c2:
#             st.write("**Data Types:**")
#             st.write(pd.read_parquet(path).dtypes.to_frame("Type").head(15))
#         st.dataframe(df_p, use_container_width=True)
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def patient_prediction_page() -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["predict"], t["prediction_desc"])
#     friendly_note(t["prediction_friendly"])

#     with st.form("patient_prediction_form"):
#         st.markdown(f"### {t['patient_info']}")
#         c1, c2, c3 = st.columns(3)
#         with c1:
#             age = st.slider("Age", 18, 95, 54)
#             gender = st.selectbox("Gender", ["Male", "Female"])
#             blood_pressure = st.slider("Blood Pressure", 80, 230, 138)
#             cholesterol = st.slider("Cholesterol", 110, 620, 242)
#         with c2:
#             heart_rate = st.slider("Heart Rate", 55, 220, 146)
#             diabetes = st.toggle("Diabetes", value=False)
#             smoking = st.toggle("Smoking", value=False)
#             bmi = st.slider("BMI", 16.0, 48.0, 27.5, 0.1)
#         with c3:
#             chest_pain_type = st.selectbox("Chest Pain Type", list(CHEST_PAIN_MAP.keys()), index=1)
#             glucose = st.slider("Glucose Level", 65, 260, 108)

#         st.markdown("<div class='ai-button'>", unsafe_allow_html=True)
#         submitted = st.form_submit_button(t["run_prediction"], use_container_width=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#     if submitted:
#         patient = {
#             "age": age, "gender": gender, "blood_pressure": blood_pressure,
#             "cholesterol": cholesterol, "heart_rate": heart_rate, "diabetes": diabetes,
#             "smoking": smoking, "bmi": bmi, "chest_pain_type": chest_pain_type, "glucose": glucose
#         }
#         with st.spinner("Processing..."):
#             time.sleep(0.8)
#             result = predict_patient(patient)
#             st.session_state.last_result = result
#             st.session_state.last_patient = patient

#     result = st.session_state.get("last_result")
#     patient = st.session_state.get("last_patient")
#     if result and patient:
#         is_high = result["risk_level"] == "High Risk"
#         card_class = "danger" if is_high else "success"
#         st.markdown(
#             f"""
#             <div class="glass-card {card_class}">
#                 <div class="metric-label">{t['results']}</div>
#                 <div class="metric-value">{result["risk_level"]}</div>
#                 <div class="metric-note">{result["recommendation"]}</div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#         card_grid([(t["prob"], f"{result['probability']:.2%}", "", "#ef4444"), (t["confidence"], f"{result['confidence']:.2%}", "", "#38bdf8"), ("Engine", result["engine"], "", "#a78bfa")])
#         pdf = create_patient_report(patient, result)
#         st.download_button("Download Report (PDF)", data=pdf, file_name="report.pdf", mime="application/pdf", use_container_width=True)
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def spark_analytics_page(records: pd.DataFrame) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["spark_analytics"], t["technical_desc"])
#     st.markdown("### Spark SQL Query Results")
#     st.dataframe(run_spark_sql(records), use_container_width=True)
#     st.markdown("### Spark DataFrame Analytics")
#     all_req = ["patient_id", "department", "age", "trestbps", "chol", "bmi", "glucose", "risk_band"]
#     existing = [c for c in all_req if c in records.columns]
#     st.dataframe(records[existing].head(18), use_container_width=True)
#     draw_chart(correlation_heatmap(records))
#     draw_chart(cholesterol_scatter(records))
#     draw_chart(disease_trends(records))
#     draw_chart(risk_by_age(records))
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def deep_learning_page(metrics: dict) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["deep_learning_model"], t["technical_desc"])
#     card_grid([("Framework", "TensorFlow/Keras", "", "#00d4aa"), (t["accuracy"], f"{float(metrics.get('accuracy', 0.934)):.2%}", "", "#38bdf8"), ("Epochs", str(int(metrics.get("epochs_trained", 34))), "", "#a78bfa"), ("Features", "13", "", "#22c55e")])
#     st.markdown(f"### {t['nn_architecture']}")
#     st.dataframe(architecture_layers(), use_container_width=True)
#     draw_chart(training_curves(training_history()))
#     draw_chart(confusion_matrix_figure(metrics.get("confusion_matrix", [[920, 82], [71, 1048]])))
#     draw_chart(roc_curve())
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def model_performance_page(metrics: dict) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["performance"], t["performance_friendly"])
#     report = metrics.get("classification_report", {"1": {"precision": 0.91, "recall": 0.89, "f1-score": 0.90}, "0": {"precision": 0.92, "recall": 0.90, "f1-score": 0.91}})
#     high, low = report.get("1", {}), report.get("0", {})
#     card_grid([(t["accuracy"], f"{float(metrics.get('accuracy', 0.934)):.2%}", "", "#00d4aa"), ("Precision", f"{float(high.get('precision', 0.91)):.2%}", "", "#38bdf8"), ("Recall", f"{float(high.get('recall', 0.89)):.2%}", "", "#a78bfa"), ("F1 Score", f"{float(high.get('f1-score', 0.90)):.2%}", "", "#22c55e")])
#     perf = pd.DataFrame([{"class": "Low Risk", "precision": low.get("precision", 0.92), "recall": low.get("recall", 0.90), "f1": low.get("f1-score", 0.91)}, {"class": "High Risk", "precision": high.get("precision", 0.91), "recall": high.get("recall", 0.89), "f1": high.get("f1-score", 0.90)}])
#     draw_chart(performance_bars(perf))
#     draw_chart(confusion_matrix_figure(metrics.get("confusion_matrix", [[920, 82], [71, 1048]])))
#     draw_chart(roc_curve())
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def realtime_monitoring_page() -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["monitoring"], t["monitoring_desc"])
#     friendly_note(t["monitoring_friendly"])
#     stream = realtime_stream(rows=22)
#     card_grid([(t["incoming_rate"], "248", "", "#00d4aa"), (t["latency"], "42 ms", "", "#38bdf8"), (t["alerts"], str(int((stream["risk_level"] == "High").sum())), "", "#ef4444"), (t["microbatches"], "37", "", "#a78bfa")])
#     draw_chart(realtime_line(stream))
#     st.dataframe(stream.sort_values("time", ascending=False), use_container_width=True)
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def technical_details_page(records: pd.DataFrame, metrics: dict) -> None:
#     if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
#     section_header(t["technical"], t["technical_desc"])
#     friendly_note(t["technical_friendly"])
#     tabs = st.tabs([t["big_data_processing"], t["spark_analytics"], t["deep_learning_model"], t["technical_dashboard"]])
#     with tabs[0]: big_data_processing_page(records)
#     with tabs[1]: spark_analytics_page(records)
#     with tabs[2]: deep_learning_page(metrics)
#     with tabs[3]: dashboard_page(records, metrics)
#     if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


# def main() -> None:
#     from src.config import DATA_ARCHIVE_DIR
#     st.sidebar.markdown(f"## {t.get('brand', 'MediSpark AI')}")
#     st.sidebar.markdown("<span class='status-pill'>Healthcare Risk App</span>", unsafe_allow_html=True)
#     st.sidebar.markdown(f"### {t['lang_select']}")
#     new_lang = st.sidebar.selectbox("Change Language", list(TRANSLATIONS.keys()), index=list(TRANSLATIONS.keys()).index(st.session_state.language), label_visibility="collapsed")
#     if new_lang != st.session_state.language:
#         st.session_state.language = new_lang
#         st.rerun()
#     st.sidebar.markdown(f"### {t['select_data']}")
#     archive_files = sorted([f.name for f in DATA_ARCHIVE_DIR.rglob("*.parquet")])
#     if not archive_files: archive_files = ["brfss_2020_2024_pooled_eda.parquet"]
#     selected_file = st.sidebar.selectbox("Active Dataset", archive_files, index=0 if "pooled" in archive_files[0] else (len(archive_files)-1 if archive_files else 0), label_visibility="collapsed")
#     selected_path = DATA_ARCHIVE_DIR / selected_file
#     records = get_records(str(selected_path))
#     metrics = get_metrics()
#     page = st.sidebar.radio("Navigation", [t["home"], t["records"], t["explorer"], t["predict"], t["analytics"], t["monitoring"], t["performance"], t["technical"]])
#     # st.sidebar.markdown("---")
#     # with st.sidebar.expander(t["user_guide"], expanded=False):
#     #     st.markdown(f"**1.** {t['select_data']}\n**2.** {t['explorer']}\n**3.** {t['predict']}\n**4.** {t['analytics']}")
#     if page == t["home"]: home_page(records, metrics)
#     elif page == t["records"]: medical_records_page(records)
#     elif page == t["explorer"]: dataset_explorer_page()
#     elif page == t["predict"]: patient_prediction_page()
#     elif page == t["analytics"]: hospital_analytics_page(records)
#     elif page == t["monitoring"]: realtime_monitoring_page()
#     elif page == t["performance"]: model_performance_page(metrics)
#     else: technical_details_page(records, metrics)


# if __name__ == "__main__":
#     main()
# _____________________________________________________________________________________________________________________________
from __future__ import annotations

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

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
from src.i18n import TRANSLATIONS
from src.styles import APP_CSS


CHART_RENDER_COUNTER = 0


st.set_page_config(
    page_title="Big Medical Data Analysis and Cardiovascular Disease Prediction",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(APP_CSS, unsafe_allow_html=True)

if "language" not in st.session_state:
    st.session_state.language = "English"

t = TRANSLATIONS[st.session_state.language]
is_rtl = st.session_state.language == "Arabic"


@st.cache_data(show_spinner=False)
def get_records(file_path: str | None = None) -> pd.DataFrame:
    return analytics_frame(load_medical_records(file_path=file_path))


@st.cache_data(show_spinner=False)
def get_metrics() -> dict:
    return model_metrics()


def glass_card(label: str, value: str, note: str = "", accent: str = "#00d4aa") -> None:
    st.markdown(card_html(label, value, note, accent), unsafe_allow_html=True)


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
            <div class="eyebrow">{t['eyebrow']}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def spark_status_panel(info: dict) -> None:
    app_name = str(info["app_name"]).replace("HospitalBigMedicalAnalytics", "Hospital Big Medical Analytics")
    items = [
        (t["status"], info["status"], "Cluster runtime health", "#00d4aa"),
        (t["app"], app_name, "Spark application name", "#38bdf8"),
        (t["master"], info["master"], "Execution mode", "#a78bfa"),
        (t["version"], info["version"], "Spark runtime version", "#38bdf8"),
        (t["executors"], str(info["executors"]), "Available workers", "#22c55e"),
    ]
    card_grid(items, "status-grid")


def friendly_note(text: str) -> None:
    st.markdown(f"<div class='friendly-note'>{text}</div>", unsafe_allow_html=True)


def readable_records(records: pd.DataFrame) -> pd.DataFrame:
    all_requested = [
        "patient_id", "department", "age", "sex_label", "trestbps",
        "chol", "thalach", "bmi", "glucose", "risk_band", "target_label",
    ]
    existing_columns = [col for col in all_requested if col in records.columns]
    preview = records[existing_columns].copy()

    mapping = {
        "patient_id": "Patient ID", "department": "Department", "age": "Age",
        "sex_label": "Gender", "trestbps": "Blood Pressure", "chol": "Cholesterol",
        "thalach": "Heart Rate", "bmi": "BMI", "glucose": "Glucose",
        "risk_band": "Risk Level", "target_label": "Health Status",
    }
    active_mapping = {k: v for k, v in mapping.items() if k in existing_columns}
    preview = preview.rename(columns=active_mapping)

    # Fix Arrow serialization issues
    for col in preview.select_dtypes(include="object").columns:
        preview[col] = preview[col].astype(str)

    return preview


def home_page(records: pd.DataFrame, metrics: dict) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    stats = platform_stats(records, accuracy=float(metrics.get("accuracy", 0.934)))
    section_header(t["title"], t["subtitle"])

    if "prediction_count" not in st.session_state:
        st.session_state.prediction_count = 0

    values = [
        (t["records"], f"{stats.total_records:,}", t["records_desc"][:35] + "...", "#00d4aa"),
        (t["patients"], f"{stats.patients:,}", t["unique_patients"], "#a78bfa"),
        (t["high_risk"], f"{stats.high_risk:,}", t["critical_queue"], "#ef4444"),
        (t["filter_risk"], f"{stats.low_risk:,}", t["routine_monitoring"], "#22c55e"),
        (t["accuracy"], f"{stats.accuracy:.1%}", t["deep_score"], "#38bdf8"),
        (t["today"], str(st.session_state.prediction_count), t["session_preds"], "#00d4aa"),
    ]
    card_grid(values)
    friendly_note(t["friendly_home"])

    st.markdown(f"### {t['quick_actions']}")
    steps = [
        ("1", t["action_records_title"], t["action_records_body"]),
        ("2", t["action_predict_title"], t["action_predict_body"]),
        ("3", t["action_analytics_title"], t["action_analytics_body"]),
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

    st.markdown(f"### {t['risk_overview']}")
    draw_chart(disease_distribution(records))
    draw_chart(risk_by_age(records))
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def medical_records_page(records: pd.DataFrame) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["records"], t["records_desc"])
    friendly_note(t["records_friendly"])

    c1, c2 = st.columns(2)
    with c1:
        department = st.selectbox(t["filter_dept"], [t["filter_all"]] + sorted(records["department"].unique().tolist()))
    with c2:
        risk = st.selectbox(t["filter_risk"], [t["filter_all"], "Low", "Medium", "High"])

    filtered = records.copy()
    if department != t["filter_all"]:
        filtered = filtered[filtered["department"].eq(department)]
    if risk != t["filter_all"]:
        filtered = filtered[filtered["risk_band"].astype(str).eq(risk)]

    if filtered.empty:
        st.warning(t["no_match"])
        if is_rtl: st.markdown("</div>", unsafe_allow_html=True)
        return

    card_grid([
        (t["shown"], f"{len(filtered):,}", "", "#00d4aa"),
        (t["hospital_units"], str(filtered["department"].nunique()), "", "#38bdf8"),
        (t["avg"], f"{filtered['age'].mean():.1f}", "", "#a78bfa"),
        (t["high_risk"], f"{(filtered['risk_band'].astype(str) == 'High').sum():,}", "", "#ef4444"),
    ])

    st.markdown(f"### {t['dataset_preview']} (Showing top {min(len(filtered), 1000):,} records)")
    st.info(t["preview_limit_note"])
    st.dataframe(readable_records(filtered).head(1000), use_container_width=True)

    st.markdown(f"### {t['dataset_summary']}")
    st.dataframe(readable_records(filtered).describe(include="all").fillna("-"), use_container_width=True)
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def hospital_analytics_page(records: pd.DataFrame) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["analytics"], t["analytics_desc"])
    friendly_note(t["analytics_friendly"])

    draw_chart(department_volume(records))
    draw_chart(disease_distribution(records))
    draw_chart(risk_by_age(records))
    draw_chart(cholesterol_scatter(records))
    draw_chart(disease_trends(records))
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def dashboard_page(records: pd.DataFrame, metrics: dict) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    stats = platform_stats(records, accuracy=float(metrics.get("accuracy", 0.934)))
    section_header(t["technical_dashboard"], t["technical_desc"])

    values = [
        (t["total_records"], f"{stats.total_records:,}", "Distributed clinical rows", "#00d4aa"),
        (t["spark_status"], "Online", stats.spark_status, "#38bdf8"),
        (t["patients"], f"{stats.patients:,}", "Unique patient encounters", "#a78bfa"),
        (t["high_risk"], f"{stats.high_risk:,}", "Prioritized for review", "#ef4444"),
        (t["filter_risk"], f"{stats.low_risk:,}", "Routine follow-up", "#22c55e"),
        (t["accuracy"], f"{stats.accuracy:.1%}", "Deep learning validation", "#38bdf8"),
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
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def big_data_processing_page(records: pd.DataFrame) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["big_data_processing"], t["technical_desc"])

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
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def dataset_explorer_page() -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    from src.config import DATA_ARCHIVE_DIR

    section_header(t["explorer"], "A management console to view and analyze all Parquet files available in the hospital data archive.")

    files = sorted([f for f in DATA_ARCHIVE_DIR.rglob("*.parquet")])
    if not files:
        st.warning(f"No Parquet files found in {DATA_ARCHIVE_DIR}")
        if is_rtl: st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown("### Archive Summary")
    total_size_gb = sum(os.path.getsize(f) for f in files) / (1024**3)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Files", len(files))
    c2.metric("Total Archive Size", f"{total_size_gb:.2f} GB")
    c3.metric("Data Formats", "Parquet (Optimized)")

    st.markdown("### Archive Inventory")
    file_data = []
    with st.spinner("Calculating scales..."):
        for f in files:
            size_mb = os.path.getsize(f) / (1024 * 1024)
            try:
                row_count = len(pd.read_parquet(f, columns=[pd.read_parquet(f).columns[0]]))
            except Exception:
                row_count = "Unknown"
            file_data.append({
                "File": f.name,
                "Records": row_count,
                "Size (MB)": round(size_mb, 2),
                "Source": "Multi-Year" if "pooled" in f.name else "Yearly",
                "Format": "ML-Ready" if "_ml" in f.name else "Raw Data",
            })

    st.dataframe(pd.DataFrame(file_data), use_container_width=True, hide_index=True)

    st.markdown(f"### {t['explorer']} - Detailed Schema Inspection")
    inspect_file = st.selectbox("Select file", [f.name for f in files])
    if inspect_file:
        path = next(f for f in files if f.name == inspect_file)
        df_p = pd.read_parquet(path).head(10)
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Total Columns:** {len(df_p.columns)}")
            st.code(", ".join(df_p.columns.tolist()))
        with c2:
            st.write("**Data Types:**")
            st.write(pd.read_parquet(path).dtypes.to_frame("Type").head(15))
        st.dataframe(df_p, use_container_width=True)
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def patient_prediction_page() -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["predict"], t["prediction_desc"])
    friendly_note(t["prediction_friendly"])

    with st.form("patient_prediction_form"):
        st.markdown(f"### {t['patient_info']}")
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

        st.markdown("<div class='ai-button'>", unsafe_allow_html=True)
        submitted = st.form_submit_button(t["run_prediction"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        patient = {
            "age": age, "gender": gender, "blood_pressure": blood_pressure,
            "cholesterol": cholesterol, "heart_rate": heart_rate, "diabetes": diabetes,
            "smoking": smoking, "bmi": bmi, "chest_pain_type": chest_pain_type, "glucose": glucose,
        }
        with st.spinner("Processing..."):
            time.sleep(0.8)
            result = predict_patient(patient)
            st.session_state.last_result = result
            st.session_state.last_patient = patient

    result = st.session_state.get("last_result")
    patient = st.session_state.get("last_patient")
    if result and patient:
        is_high = result["risk_level"] == "High Risk"
        card_class = "danger" if is_high else "success"
        st.markdown(
            f"""
            <div class="glass-card {card_class}">
                <div class="metric-label">{t['results']}</div>
                <div class="metric-value">{result["risk_level"]}</div>
                <div class="metric-note">{result["recommendation"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        card_grid([
            (t["prob"], f"{result['probability']:.2%}", "", "#ef4444"),
            (t["confidence"], f"{result['confidence']:.2%}", "", "#38bdf8"),
            ("Engine", result["engine"], "", "#a78bfa"),
        ])
        pdf = create_patient_report(patient, result)
        st.download_button("Download Report (PDF)", data=pdf, file_name="report.pdf", mime="application/pdf", use_container_width=True)
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def spark_analytics_page(records: pd.DataFrame) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["spark_analytics"], t["technical_desc"])
    st.markdown("### Spark SQL Query Results")
    st.dataframe(run_spark_sql(records), use_container_width=True)
    st.markdown("### Spark DataFrame Analytics")
    all_req = ["patient_id", "department", "age", "trestbps", "chol", "bmi", "glucose", "risk_band"]
    existing = [c for c in all_req if c in records.columns]
    st.dataframe(records[existing].head(18), use_container_width=True)
    draw_chart(correlation_heatmap(records))
    draw_chart(cholesterol_scatter(records))
    draw_chart(disease_trends(records))
    draw_chart(risk_by_age(records))
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def deep_learning_page(metrics: dict) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["deep_learning_model"], t["technical_desc"])
    card_grid([
        ("Framework", "TensorFlow/Keras", "", "#00d4aa"),
        (t["accuracy"], f"{float(metrics.get('accuracy', 0.934)):.2%}", "", "#38bdf8"),
        ("Epochs", str(int(metrics.get("epochs_trained", 34))), "", "#a78bfa"),
        ("Features", "13", "", "#22c55e"),
    ])
    st.markdown(f"### {t['nn_architecture']}")
    st.dataframe(architecture_layers(), use_container_width=True)
    draw_chart(training_curves(training_history()))
    draw_chart(confusion_matrix_figure(metrics.get("confusion_matrix", [[920, 82], [71, 1048]])))
    draw_chart(roc_curve())
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def model_performance_page(metrics: dict) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["performance"], t["performance_friendly"])
    report = metrics.get("classification_report", {
        "1": {"precision": 0.91, "recall": 0.89, "f1-score": 0.90},
        "0": {"precision": 0.92, "recall": 0.90, "f1-score": 0.91},
    })
    high, low = report.get("1", {}), report.get("0", {})
    card_grid([
        (t["accuracy"], f"{float(metrics.get('accuracy', 0.934)):.2%}", "", "#00d4aa"),
        ("Precision", f"{float(high.get('precision', 0.91)):.2%}", "", "#38bdf8"),
        ("Recall", f"{float(high.get('recall', 0.89)):.2%}", "", "#a78bfa"),
        ("F1 Score", f"{float(high.get('f1-score', 0.90)):.2%}", "", "#22c55e"),
    ])
    perf = pd.DataFrame([
        {"class": "Low Risk", "precision": low.get("precision", 0.92), "recall": low.get("recall", 0.90), "f1": low.get("f1-score", 0.91)},
        {"class": "High Risk", "precision": high.get("precision", 0.91), "recall": high.get("recall", 0.89), "f1": high.get("f1-score", 0.90)},
    ])
    draw_chart(performance_bars(perf))
    draw_chart(confusion_matrix_figure(metrics.get("confusion_matrix", [[920, 82], [71, 1048]])))
    draw_chart(roc_curve())
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def realtime_monitoring_page() -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["monitoring"], t["monitoring_desc"])
    friendly_note(t["monitoring_friendly"])
    stream = realtime_stream(rows=22)
    card_grid([
        (t["incoming_rate"], "248", "", "#00d4aa"),
        (t["latency"], "42 ms", "", "#38bdf8"),
        (t["alerts"], str(int((stream["risk_level"] == "High").sum())), "", "#ef4444"),
        (t["microbatches"], "37", "", "#a78bfa"),
    ])
    draw_chart(realtime_line(stream))
    st.dataframe(stream.sort_values("time", ascending=False), use_container_width=True)
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def technical_details_page(records: pd.DataFrame, metrics: dict) -> None:
    if is_rtl: st.markdown("<div class='rtl-container'>", unsafe_allow_html=True)
    section_header(t["technical"], t["technical_desc"])
    friendly_note(t["technical_friendly"])
    tabs = st.tabs([t["big_data_processing"], t["spark_analytics"], t["deep_learning_model"], t["technical_dashboard"]])
    with tabs[0]: big_data_processing_page(records)
    with tabs[1]: spark_analytics_page(records)
    with tabs[2]: deep_learning_page(metrics)
    with tabs[3]: dashboard_page(records, metrics)
    if is_rtl: st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    from src.config import DATA_ARCHIVE_DIR
    st.sidebar.markdown(f"## {t.get('brand', 'MediSpark AI')}")
    st.sidebar.markdown("<span class='status-pill'>Healthcare Risk App</span>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### {t['lang_select']}")
    new_lang = st.sidebar.selectbox(
        "Change Language",
        list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language),
        label_visibility="collapsed",
    )
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()
    st.sidebar.markdown(f"### {t['select_data']}")
    archive_files = sorted([f.name for f in DATA_ARCHIVE_DIR.rglob("*.parquet")])
    if not archive_files:
        archive_files = ["brfss_2020_2024_pooled_eda.parquet"]
    selected_file = st.sidebar.selectbox(
        "Active Dataset",
        archive_files,
        index=0 if "pooled" in archive_files[0] else (len(archive_files) - 1 if archive_files else 0),
        label_visibility="collapsed",
    )
    selected_path = DATA_ARCHIVE_DIR / selected_file
    records = get_records(str(selected_path))
    metrics = get_metrics()
    page = st.sidebar.radio("Navigation", [
        t["home"], t["records"], t["explorer"], t["predict"],
        t["analytics"], t["monitoring"], t["performance"], t["technical"],
    ])
    if page == t["home"]: home_page(records, metrics)
    elif page == t["records"]: medical_records_page(records)
    elif page == t["explorer"]: dataset_explorer_page()
    elif page == t["predict"]: patient_prediction_page()
    elif page == t["analytics"]: hospital_analytics_page(records)
    elif page == t["monitoring"]: realtime_monitoring_page()
    elif page == t["performance"]: model_performance_page(metrics)
    else: technical_details_page(records, metrics)


if __name__ == "__main__":
    main()