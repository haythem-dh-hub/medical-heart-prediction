from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from src.config import FEATURES_PATH, MODEL_DIR, MODEL_PATH
from src.data_loader import load_dataset
from src.preprocess import prepare_features
from src.reporting import save_metrics


def train_and_save_model() -> None:
    dataframe = load_dataset()
    x, y = prepare_features(dataframe)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    best_name = ""
    best_score = -1.0
    best_model = None
    best_metrics = None

    for name, model in models.items():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        score = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions, zero_division=0, output_dict=True)
        matrix = confusion_matrix(y_test, predictions).tolist()

        print(f"\nModel: {name}")
        print(f"Accuracy: {score:.4f}")
        print(classification_report(y_test, predictions, zero_division=0))

        if score > best_score:
            best_score = score
            best_name = name
            best_model = model
            best_metrics = {
                "best_model": name,
                "accuracy": score,
                "classification_report": report,
                "confusion_matrix": matrix,
                "dataset_rows": int(len(dataframe)),
                "train_rows": int(len(x_train)),
                "test_rows": int(len(x_test)),
                "features": list(x.columns),
            }

    if best_model is None or best_metrics is None:
        raise RuntimeError("No model was trained.")

    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(list(x.columns), FEATURES_PATH)
    save_metrics(best_metrics)

    print(f"\nBest model: {best_name}")
    print(f"Saved model to: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()
