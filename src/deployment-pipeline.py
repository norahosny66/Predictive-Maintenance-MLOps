# src/pipeline.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # add project root

from prefect import flow, task
from src.extract_features import extract_features_main
from src.train import train_model_main

@task
def extract_features():
    extract_features_main()  # Your existing function

@task
def train_model():
    train_model_main()  # Your existing function

@flow(name="Bearing Failure Prediction Pipeline")
def full_pipeline():
    print("Starting Feature Extraction...")
    extract_features()
    print("Feature Extraction Done!")

    print("Starting Model Training...")
    train_model()
    print("Model Training Done!")

if __name__ == "__main__":
    full_pipeline()
