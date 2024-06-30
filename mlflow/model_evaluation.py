
from sklearn import ensemble
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
import mlflow
from mlflow.models import infer_signature
from mlflow.models import MetricThreshold
# from mlflow.exceptions import ModelValidationFailedException
import shap
import pandas as pd
import xgboost
import joblib
import numpy as np
import os

model_base = '/Users/drjosefhartmann/Development/Accidents/may24_bmlops_accidents/airflow/Volumes/models'
data_base = '/Users/drjosefhartmann/Development/Accidents/may24_bmlops_accidents/airflow/Volumes/data'

# LOAD DATA
X_train = pd.read_csv(data_base + '/preprocessed/X_train.csv')
X_test = pd.read_csv(data_base + '/preprocessed/X_test.csv')
y_train = pd.read_csv(data_base + '/preprocessed/y_train.csv')
y_test = pd.read_csv(data_base + '/preprocessed/y_test.csv')
y_train = np.ravel(y_train)
y_test = np.ravel(y_test)

# train a candidate XGBoost model
# candidate_model = ensemble.RandomForestClassifier(n_jobs=-1).fit(X_train, y_train)
candidate_model = xgboost.XGBClassifier().fit(X_train, y_train)
# train a baseline dummy model
baseline_model = DummyClassifier(strategy="uniform").fit(X_train, y_train)

# create signature that is shared by the two models
signature = infer_signature(X_test, y_test)

# construct an evaluation dataset from the test set
eval_data = X_test
eval_data["label"] = y_test

# Define criteria for model to be validated against


def evaluate_model(candidate_model = candidate_model, baseline_model = baseline_model, eval_data = eval_data):
    thresholds = {
    "accuracy_score": MetricThreshold(
        threshold=0.8,  # accuracy should be >=0.8
        min_absolute_change=0.05,  # accuracy should be at least 0.05 greater than baseline model accuracy
        min_relative_change=0.05,  # accuracy should be at least 5 percent greater than baseline model accuracy
        greater_is_better=True,
    ),
    }   
    with mlflow.start_run() as run:
        candidate_model_uri = mlflow.sklearn.log_model(
            candidate_model, "candidate_model", signature=signature
        ).model_uri
        baseline_model_uri = mlflow.sklearn.log_model(
            baseline_model, "baseline_model", signature=signature
        ).model_uri
        try:
            mlflow.evaluate(
                candidate_model_uri,
                eval_data,
                targets="label",
                model_type="classifier",
                # evaluators="accuracy",
                validation_thresholds=thresholds,
                baseline_model=baseline_model_uri,
            )
            return 1
        except :
            print("Model validation failed")
            return 0




        

    
