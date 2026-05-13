from pathlib import Path

import joblib
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.config import (
    DEEP_METRICS_PATH,
    DEEP_MODEL_PATH,
    DEEP_SCALER_PATH,
    FEATURES_PATH,
    MODEL_DIR,
)
from src.data_loader import load_dataset
from src.preprocess import prepare_features
from src.reporting import save_metrics_to_path


def build_deep_model(input_dim: int) -> tf.keras.Model:
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(input_dim,)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_deep_model() -> None:
    dataframe = load_dataset()
    x, y = prepare_features(dataframe)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = build_deep_model(x_train.shape[1])
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=10, restore_best_weights=True
    )

    history = model.fit(
        x_train_scaled,
        y_train,
        validation_split=0.2,
        epochs=100,
        batch_size=8,
        verbose=0,
        callbacks=[early_stopping],
    )

    probabilities = model.predict(x_test_scaled, verbose=0).flatten()
    predictions = (probabilities >= 0.5).astype(int)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, zero_division=0, output_dict=True)
    matrix = confusion_matrix(y_test, predictions).tolist()

    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    model.save(DEEP_MODEL_PATH)
    joblib.dump(scaler, DEEP_SCALER_PATH)
    joblib.dump(list(x.columns), FEATURES_PATH)

    metrics = {
        "best_model": "tensorflow_deep_neural_network",
        "accuracy": float(accuracy),
        "classification_report": report,
        "confusion_matrix": matrix,
        "dataset_rows": int(len(dataframe)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "features": list(x.columns),
        "epochs_trained": int(len(history.history["loss"])),
    }
    save_metrics_to_path(DEEP_METRICS_PATH, metrics)

    print(f"Deep learning model saved to: {DEEP_MODEL_PATH}")
    print(f"Deep learning metrics saved to: {DEEP_METRICS_PATH}")


if __name__ == "__main__":
    train_deep_model()
