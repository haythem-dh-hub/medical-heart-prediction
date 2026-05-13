from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession

from src.config import RAW_DATA_PATH, SPARK_METRICS_PATH, TARGET_COLUMN
from src.reporting import save_metrics_to_path


def train_spark_models() -> None:
    spark = (
        SparkSession.builder.appName("HeartDiseaseSparkTraining")
        .master("local[*]")
        .getOrCreate()
    )

    dataframe = spark.read.parquet(str(RAW_DATA_PATH))
    feature_columns = [column for column in dataframe.columns if column != TARGET_COLUMN]

    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    prepared = assembler.transform(dataframe).select("features", TARGET_COLUMN)
    train_df, test_df = prepared.randomSplit([0.8, 0.2], seed=42)

    models = {
        "spark_logistic_regression": LogisticRegression(
            featuresCol="features", labelCol=TARGET_COLUMN
        ),
        "spark_random_forest": RandomForestClassifier(
            featuresCol="features", labelCol=TARGET_COLUMN, numTrees=50, seed=42
        ),
    }

    auc_evaluator = BinaryClassificationEvaluator(
        labelCol=TARGET_COLUMN, rawPredictionCol="rawPrediction", metricName="areaUnderROC"
    )
    accuracy_evaluator = MulticlassClassificationEvaluator(
        labelCol=TARGET_COLUMN, predictionCol="prediction", metricName="accuracy"
    )

    best_name = ""
    best_auc = -1.0
    best_metrics = None

    for name, classifier in models.items():
        pipeline = Pipeline(stages=[classifier])
        model = pipeline.fit(train_df)
        predictions = model.transform(test_df)

        auc = auc_evaluator.evaluate(predictions)
        accuracy = accuracy_evaluator.evaluate(predictions)

        if auc > best_auc:
            best_auc = auc
            best_name = name
            best_metrics = {
                "best_model": name,
                "accuracy": float(accuracy),
                "auc": float(auc),
                "dataset_rows": int(dataframe.count()),
                "train_rows": int(train_df.count()),
                "test_rows": int(test_df.count()),
                "features": feature_columns,
                "framework": "Apache Spark MLlib",
            }

    if best_metrics is None:
        spark.stop()
        raise RuntimeError("Spark training failed to produce metrics.")

    save_metrics_to_path(SPARK_METRICS_PATH, best_metrics)
    spark.stop()

    print(f"Best Spark model: {best_name}")
    print(f"Spark metrics saved to: {SPARK_METRICS_PATH}")


if __name__ == "__main__":
    train_spark_models()
