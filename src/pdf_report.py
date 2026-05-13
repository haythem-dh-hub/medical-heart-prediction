from __future__ import annotations

from datetime import datetime
from typing import Any


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _pdf_lines(lines: list[str]) -> str:
    y = 760
    commands = ["BT", "/F1 12 Tf", "72 760 Td"]
    for index, line in enumerate(lines):
        if index == 0:
            commands.append(f"({_escape(line)}) Tj")
        else:
            y_step = 18
            commands.append(f"0 -{y_step} Td ({_escape(line)}) Tj")
            y -= y_step
            if y < 70:
                break
    commands.append("ET")
    return "\n".join(commands)


def create_patient_report(patient: dict[str, Any], result: dict[str, Any]) -> bytes:
    """Create a tiny standards-compliant PDF without requiring extra packages."""
    lines = [
        "Big Medical Data Analysis and Cardiovascular Disease Prediction",
        "AI Patient Risk Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Age: {patient.get('age')}",
        f"Gender: {patient.get('gender')}",
        f"Blood Pressure: {patient.get('blood_pressure')} mmHg",
        f"Cholesterol: {patient.get('cholesterol')} mg/dL",
        f"Heart Rate: {patient.get('heart_rate')} bpm",
        f"Diabetes: {'Yes' if patient.get('diabetes') else 'No'}",
        f"Smoking: {'Yes' if patient.get('smoking') else 'No'}",
        f"BMI: {patient.get('bmi')}",
        f"Glucose Level: {patient.get('glucose')} mg/dL",
        "",
        f"Prediction: {result.get('risk_level')}",
        f"Risk Probability: {result.get('probability', 0):.2%}",
        f"AI Confidence: {result.get('confidence', 0):.2%}",
        f"Model Engine: {result.get('engine')}",
        f"Spark Pipeline: {result.get('spark_pipeline')}",
        "",
        "Recommendation:",
        str(result.get("recommendation", "")),
        "",
        "Educational prototype only. It does not replace professional medical advice.",
    ]

    stream = _pdf_lines(lines)
    objects = [
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n",
        "4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
        f"5 0 obj << /Length {len(stream.encode('latin-1', errors='replace'))} >> stream\n"
        f"{stream}\nendstream endobj\n",
    ]
    pdf = "%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf.encode("latin-1")))
        pdf += obj
    xref_start = len(pdf.encode("latin-1"))
    pdf += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n"
    for offset in offsets[1:]:
        pdf += f"{offset:010d} 00000 n \n"
    pdf += (
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_start}\n%%EOF"
    )
    return pdf.encode("latin-1", errors="replace")
