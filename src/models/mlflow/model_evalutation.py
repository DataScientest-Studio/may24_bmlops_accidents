import pandas as pd 
from sklearn import ensemble
import joblib
import numpy as np
import sklearn.metrics as metrics
import pickle
import json
import mlflow
from mlflow.tracking import MlflowClient

#Define tracking_uri
client = MlflowClient(tracking_uri="http://127.0.0.1:8080")

# Define experiment name
mlflow.set_experiment("Int_Accident_Model")

def evaluate():
    print("Model Evaluation")
    X_test = pd.read_csv("data/processed/X_test.csv", index_col = "date")
    y_test = pd.read_csv("data/processed/y_test.csv", index_col = "date")
    y_test = y_test.values.ravel()

    # model = ensemble.RandomForestClassifier(n_jobs = -1)
    model = pickle.load(open("models/gbr_model.pkl", "rb"))
    predictions = model.predict(X_test)

    prediction_csv = pd.DataFrame({"target_labels": y_test,
                                   "predicted_labels": predictions})

    prediction_csv.to_csv("data/prediction.csv", index=False)

    mse = metrics.mean_squared_error(y_test, predictions)
    r2 = metrics.r2_score(y_test, predictions)
        
     # Save metrics to JSON
    with open("metrics/scores.json", "w") as fd:
        json.dump({"mse": mse, "r2": r2}, fd, indent=4)

    # Log metrics and artifacts to MLflow
    with mlflow.start_run(run_name="first_run"):
        # Log metrics
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        # Log prediction CSV
        mlflow.log_artifact("data/prediction.csv")
        
        # Log metrics JSON
        mlflow.log_artifact("metrics/scores.json")

    evaluate()
