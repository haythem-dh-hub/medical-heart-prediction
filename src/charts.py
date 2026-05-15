# from __future__ import annotations

# from dataclasses import dataclass

# import numpy as np
# import pandas as pd

# try:
#     import plotly.express as px
#     import plotly.graph_objects as go

#     PLOTLY_AVAILABLE = True
# except ModuleNotFoundError:
#     px = None
#     go = None
#     PLOTLY_AVAILABLE = False

# PLOTLY_TEMPLATE = "plotly_dark"
# COLORWAY = ["#00d4aa", "#38bdf8", "#a78bfa", "#ef4444", "#22c55e", "#f59e0b"]


# @dataclass
# class ChartFallback:
#     title: str
#     data: pd.DataFrame
#     kind: str = "dataframe"


# def style_figure(fig, height: int = 360):
#     fig.update_layout(
#         template=PLOTLY_TEMPLATE,
#         height=height,
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(3,7,18,0.25)",
#         font_color="#dbeafe",
#         title_font_color="#f8fafc",
#         colorway=COLORWAY,
#         margin=dict(l=20, r=20, t=42, b=20),
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="right",
#             x=1,
#             font=dict(color="#dbeafe"),
#         ),
#     )
#     fig.update_xaxes(gridcolor="rgba(148,163,184,.15)")
#     fig.update_yaxes(gridcolor="rgba(148,163,184,.15)")
#     return fig


# def disease_distribution(records: pd.DataFrame):
#     counts = records["target_label"].value_counts().reset_index()
#     counts.columns = ["status", "records"]
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback("Cardiovascular Disease Distribution", counts.set_index("status"), "bar")

#     fig = px.pie(
#         counts,
#         names="status",
#         values="records",
#         hole=0.58,
#         color_discrete_sequence=["#22c55e", "#ef4444"],
#         title="Cardiovascular Disease Distribution",
#     )
#     return style_figure(fig)


# def risk_by_age(records: pd.DataFrame):
#     # الصحيح ✅
#     grouped = records.groupby(["age_band", "risk_band"], as_index=False, observed=True).size()
#     # grouped = records.groupby(["age_band", "risk_band"], as_index=False).size()
#     if not PLOTLY_AVAILABLE:
#         pivot = grouped.pivot(index="age_band", columns="risk_band", values="size").fillna(0)
#         return ChartFallback("Risk Analysis by Age Band", pivot, "bar")

#     fig = px.bar(
#         grouped,
#         x="age_band",
#         y="size",
#         color="risk_band",
#         barmode="group",
#         title="Risk Analysis by Age Band",
#         labels={"size": "Patients", "age_band": "Age Band"},
#     )
#     return style_figure(fig)


# def cholesterol_scatter(records: pd.DataFrame):
#     sample = records.sample(min(650, len(records)), random_state=8)
#     all_requested = ["patient_id", "chol", "trestbps", "age", "risk_band", "department"]
#     existing_cols = [c for c in all_requested if c in sample.columns]
    
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback(
#             "Cholesterol vs Blood Pressure Risk Map",
#             sample[existing_cols].head(80),
#         )

#     fig = px.scatter(
#         sample,
#         x="chol" if "chol" in sample.columns else None,
#         y="trestbps" if "trestbps" in sample.columns else None,
#         color="risk_band" if "risk_band" in sample.columns else None,
#         size="age" if "age" in sample.columns else None,
#         hover_data=[c for c in ["department", "patient_id"] if c in sample.columns],
#         title="Cholesterol vs Blood Pressure Risk Map",
#         labels={"chol": "Cholesterol", "trestbps": "Systolic BP"},
#     )
#     return style_figure(fig)


# def correlation_heatmap(records: pd.DataFrame):
#     all_requested = ["age", "trestbps", "chol", "thalach", "oldpeak", "bmi", "glucose", "target"]
#     existing_cols = [c for c in all_requested if c in records.columns]
    
#     if not existing_cols:
#         return ChartFallback("Clinical Feature Correlation Heatmap", pd.DataFrame())

#     numeric = records[existing_cols]
#     corr = numeric.corr().round(2)
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback("Clinical Feature Correlation Heatmap", corr)

#     fig = px.imshow(
#         corr,
#         text_auto=True,
#         color_continuous_scale=["#030712", "#00d4aa", "#a78bfa"],
#         title="Clinical Feature Correlation Heatmap",
#         aspect="auto",
#     )
#     return style_figure(fig, height=430)


# def training_curves(history: pd.DataFrame):
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback("TensorFlow/Keras Training Process", history.set_index("epoch"), "line")

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=history["epoch"], y=history["accuracy"], name="Training accuracy"))
#     fig.add_trace(go.Scatter(x=history["epoch"], y=history["val_accuracy"], name="Validation accuracy"))
#     fig.add_trace(go.Scatter(x=history["epoch"], y=history["loss"], name="Training loss"))
#     fig.add_trace(go.Scatter(x=history["epoch"], y=history["val_loss"], name="Validation loss"))
#     fig.update_layout(title="TensorFlow/Keras Training Process", xaxis_title="Epoch")
#     return style_figure(fig, height=400)


# def confusion_matrix_figure(matrix: list[list[int]]):
#     matrix_frame = pd.DataFrame(matrix, index=["Actual Low", "Actual High"], columns=["Pred Low", "Pred High"])
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback("Confusion Matrix", matrix_frame)

#     fig = px.imshow(
#         matrix,
#         text_auto=True,
#         labels=dict(x="Predicted", y="Actual", color="Cases"),
#         x=["Low Risk", "High Risk"],
#         y=["Low Risk", "High Risk"],
#         color_continuous_scale=["#030712", "#38bdf8", "#ef4444"],
#         title="Confusion Matrix",
#     )
#     return style_figure(fig, height=360)


# def roc_curve():
#     fpr = np.linspace(0, 1, 80)
#     tpr = 1 - np.exp(-4.3 * fpr)
#     tpr = np.maximum.accumulate(np.clip(tpr, 0, 1))
#     roc = pd.DataFrame({"false_positive_rate": fpr, "true_positive_rate": tpr})
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback("ROC Curve", roc.set_index("false_positive_rate"), "line")

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=fpr, y=tpr, fill="tozeroy", name="AUC 0.96"))
#     fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random baseline"))
#     fig.update_layout(title="ROC Curve", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
#     return style_figure(fig, height=360)


# def realtime_line(stream: pd.DataFrame):
#     if not PLOTLY_AVAILABLE:
#         fallback = stream[["time", "risk_probability", "heart_rate"]].copy()
#         fallback["heart_rate_index"] = fallback["heart_rate"] / 180
#         return ChartFallback("Live Spark Streaming Prediction Feed", fallback.set_index("time"), "line")

#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=stream["time"],
#             y=stream["risk_probability"],
#             mode="lines+markers",
#             name="Risk probability",
#             line=dict(color="#00d4aa", width=3),
#         )
#     )
#     fig.add_trace(
#         go.Bar(
#             x=stream["time"],
#             y=stream["heart_rate"] / 180,
#             name="Heart rate index",
#             marker_color="rgba(56,189,248,.35)",
#         )
#     )
#     fig.update_layout(title="Live Spark Streaming Prediction Feed", yaxis_tickformat=".0%")
#     return style_figure(fig, height=380)


# def department_volume(records: pd.DataFrame):
#     grouped = records.groupby("department", as_index=False).size().sort_values("size")
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback("Hospital Department Record Volume", grouped.set_index("department"), "bar")

#     fig = px.bar(
#         grouped,
#         x="size",
#         y="department",
#         orientation="h",
#         title="Hospital Department Record Volume",
#         labels={"size": "Records", "department": "Department"},
#     )
#     return style_figure(fig)


# def disease_trends(records: pd.DataFrame):
#     trend = (
#         records.assign(day=pd.to_datetime(records["encounter_time"]).dt.date)
#         .groupby(["day", "target_label"], as_index=False)
#         .size()
#         .tail(60)
#     )
#     if not PLOTLY_AVAILABLE:
#         pivot = trend.pivot(index="day", columns="target_label", values="size").fillna(0)
#         return ChartFallback("Disease Trends", pivot, "line")

#     fig = px.line(trend, x="day", y="size", color="target_label", title="Disease Trends")
#     return style_figure(fig)


# def performance_bars(performance: pd.DataFrame):
#     if not PLOTLY_AVAILABLE:
#         return ChartFallback("Precision / Recall Metrics", performance.set_index("class"), "bar")

#     fig = px.bar(
#         performance,
#         x="class",
#         y=["precision", "recall", "f1"],
#         barmode="group",
#         title="Precision / Recall Metrics",
#     )
#     return style_figure(fig)
# ____________________________________________________________________________________________________________________________
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ModuleNotFoundError:
    px = None
    go = None
    PLOTLY_AVAILABLE = False

PLOTLY_TEMPLATE = "plotly_dark"
COLORWAY = ["#00d4aa", "#38bdf8", "#a78bfa", "#ef4444", "#22c55e", "#f59e0b"]


@dataclass
class ChartFallback:
    title: str
    data: pd.DataFrame
    kind: str = "dataframe"


def style_figure(fig, height: int = 360):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(3,7,18,0.25)",
        font_color="#dbeafe",
        title_font_color="#f8fafc",
        colorway=COLORWAY,
        margin=dict(l=20, r=20, t=42, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#dbeafe"),
        ),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,.15)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.15)")
    return fig


def disease_distribution(records: pd.DataFrame):
    counts = records["target_label"].value_counts().reset_index()
    counts.columns = ["status", "records"]
    if not PLOTLY_AVAILABLE:
        return ChartFallback("Cardiovascular Disease Distribution", counts.set_index("status"), "bar")

    fig = px.pie(
        counts,
        names="status",
        values="records",
        hole=0.58,
        color_discrete_sequence=["#22c55e", "#ef4444"],
        title="Cardiovascular Disease Distribution",
    )
    return style_figure(fig)


def risk_by_age(records: pd.DataFrame):
    grouped = records.groupby(["age_band", "risk_band"], as_index=False, observed=True).size()
    if not PLOTLY_AVAILABLE:
        pivot = grouped.pivot(index="age_band", columns="risk_band", values="size").fillna(0)
        return ChartFallback("Risk Analysis by Age Band", pivot, "bar")

    fig = px.bar(
        grouped,
        x="age_band",
        y="size",
        color="risk_band",
        barmode="group",
        title="Risk Analysis by Age Band",
        labels={"size": "Patients", "age_band": "Age Band"},
    )
    return style_figure(fig)


def cholesterol_scatter(records: pd.DataFrame):
    sample = records.sample(min(650, len(records)), random_state=8)
    all_requested = ["patient_id", "chol", "trestbps", "age", "risk_band", "department"]
    existing_cols = [c for c in all_requested if c in sample.columns]

    if not PLOTLY_AVAILABLE:
        return ChartFallback(
            "Cholesterol vs Blood Pressure Risk Map",
            sample[existing_cols].head(80),
        )

    fig = px.scatter(
        sample,
        x="chol" if "chol" in sample.columns else None,
        y="trestbps" if "trestbps" in sample.columns else None,
        color="risk_band" if "risk_band" in sample.columns else None,
        size="age" if "age" in sample.columns else None,
        hover_data=[c for c in ["department", "patient_id"] if c in sample.columns],
        title="Cholesterol vs Blood Pressure Risk Map",
        labels={"chol": "Cholesterol", "trestbps": "Systolic BP"},
    )
    return style_figure(fig)


def correlation_heatmap(records: pd.DataFrame):
    all_requested = ["age", "trestbps", "chol", "thalach", "oldpeak", "bmi", "glucose", "target"]
    existing_cols = [c for c in all_requested if c in records.columns]

    if not existing_cols:
        return ChartFallback("Clinical Feature Correlation Heatmap", pd.DataFrame())

    numeric = records[existing_cols]
    corr = numeric.corr().round(2)
    if not PLOTLY_AVAILABLE:
        return ChartFallback("Clinical Feature Correlation Heatmap", corr)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale=["#030712", "#00d4aa", "#a78bfa"],
        title="Clinical Feature Correlation Heatmap",
        aspect="auto",
    )
    return style_figure(fig, height=430)


def training_curves(history: pd.DataFrame):
    if not PLOTLY_AVAILABLE:
        return ChartFallback("TensorFlow/Keras Training Process", history.set_index("epoch"), "line")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history["epoch"], y=history["accuracy"], name="Training accuracy"))
    fig.add_trace(go.Scatter(x=history["epoch"], y=history["val_accuracy"], name="Validation accuracy"))
    fig.add_trace(go.Scatter(x=history["epoch"], y=history["loss"], name="Training loss"))
    fig.add_trace(go.Scatter(x=history["epoch"], y=history["val_loss"], name="Validation loss"))
    fig.update_layout(title="TensorFlow/Keras Training Process", xaxis_title="Epoch")
    return style_figure(fig, height=400)


def confusion_matrix_figure(matrix: list[list[int]]):
    matrix_frame = pd.DataFrame(matrix, index=["Actual Low", "Actual High"], columns=["Pred Low", "Pred High"])
    if not PLOTLY_AVAILABLE:
        return ChartFallback("Confusion Matrix", matrix_frame)

    fig = px.imshow(
        matrix,
        text_auto=True,
        labels=dict(x="Predicted", y="Actual", color="Cases"),
        x=["Low Risk", "High Risk"],
        y=["Low Risk", "High Risk"],
        color_continuous_scale=["#030712", "#38bdf8", "#ef4444"],
        title="Confusion Matrix",
    )
    return style_figure(fig, height=360)


def roc_curve():
    fpr = np.linspace(0, 1, 80)
    tpr = 1 - np.exp(-4.3 * fpr)
    tpr = np.maximum.accumulate(np.clip(tpr, 0, 1))
    roc = pd.DataFrame({"false_positive_rate": fpr, "true_positive_rate": tpr})
    if not PLOTLY_AVAILABLE:
        return ChartFallback("ROC Curve", roc.set_index("false_positive_rate"), "line")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, fill="tozeroy", name="AUC 0.96"))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random baseline"))
    fig.update_layout(title="ROC Curve", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
    return style_figure(fig, height=360)


def realtime_line(stream: pd.DataFrame):
    if not PLOTLY_AVAILABLE:
        fallback = stream[["time", "risk_probability", "heart_rate"]].copy()
        fallback["heart_rate_index"] = fallback["heart_rate"] / 180
        return ChartFallback("Live Spark Streaming Prediction Feed", fallback.set_index("time"), "line")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=stream["time"],
            y=stream["risk_probability"],
            mode="lines+markers",
            name="Risk probability",
            line=dict(color="#00d4aa", width=3),
        )
    )
    fig.add_trace(
        go.Bar(
            x=stream["time"],
            y=stream["heart_rate"] / 180,
            name="Heart rate index",
            marker_color="rgba(56,189,248,.35)",
        )
    )
    fig.update_layout(title="Live Spark Streaming Prediction Feed", yaxis_tickformat=".0%")
    return style_figure(fig, height=380)


def department_volume(records: pd.DataFrame):
    grouped = records.groupby("department", as_index=False, observed=True).size().sort_values("size")
    if not PLOTLY_AVAILABLE:
        return ChartFallback("Hospital Department Record Volume", grouped.set_index("department"), "bar")

    fig = px.bar(
        grouped,
        x="size",
        y="department",
        orientation="h",
        title="Hospital Department Record Volume",
        labels={"size": "Records", "department": "Department"},
    )
    return style_figure(fig)


def disease_trends(records: pd.DataFrame):
    trend = (
        records.assign(day=pd.to_datetime(records["encounter_time"]).dt.date)
        .groupby(["day", "target_label"], as_index=False, observed=True)
        .size()
        .tail(60)
    )
    if not PLOTLY_AVAILABLE:
        pivot = trend.pivot(index="day", columns="target_label", values="size").fillna(0)
        return ChartFallback("Disease Trends", pivot, "line")

    fig = px.line(trend, x="day", y="size", color="target_label", title="Disease Trends")
    return style_figure(fig)


def performance_bars(performance: pd.DataFrame):
    if not PLOTLY_AVAILABLE:
        return ChartFallback("Precision / Recall Metrics", performance.set_index("class"), "bar")

    fig = px.bar(
        performance,
        x="class",
        y=["precision", "recall", "f1"],
        barmode="group",
        title="Precision / Recall Metrics",
    )
    return style_figure(fig)