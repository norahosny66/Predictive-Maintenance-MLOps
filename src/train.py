import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def load_data():
    df = pd.read_csv("data/processed/features.csv")
    X = df.drop(columns=["filename", "source", "label"], errors='ignore')
    y = df["label"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_log_model(X_train, X_test, y_train, y_test, depth):
    clf = RandomForestClassifier(n_estimators=100, max_depth=depth, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    mlflow.log_param("max_depth", depth)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(clf, "model")

    print(f"Trained model with depth={depth} → accuracy={acc:.4f}")
    return acc, clf

def promote_best_model(run_id, acc, model_name, client):
    result = mlflow.register_model(
        model_uri=f"runs:/{run_id}/model",
        name=model_name
    )
    client.set_model_version_tag(
        name=model_name,
        version=result.version,
        key="deployment_stage",
        value="production"
    )
    print(f"Model v{result.version} promoted to Production")

def train_model_main():
    mlflow.set_experiment("bearing_failure_prediction")
    mlflow.set_tracking_uri("file:/home/predictive_maintenance_project/mlruns")

    print("MLflow tracking URI:", mlflow.get_tracking_uri())

    model_name = "bearing-failure-model"
    client = mlflow.tracking.MlflowClient()

    X_train, X_test, y_train, y_test = load_data()
    best_acc = 0
    best_run_id = None

    for depth in [5, 10, 15]:
        with mlflow.start_run() as run:
            acc, _ = train_and_log_model(X_train, X_test, y_train, y_test, depth)
            if acc > best_acc:
                best_acc = acc
                best_run_id = run.info.run_id

    print(f"\nBest model accuracy: {best_acc:.4f} from run {best_run_id}")

    try:
        prod_model = client.get_latest_versions(model_name, stages=["Production"])[0]
        prod_acc = float(client.get_run(prod_model.run_id).data.metrics.get("accuracy", 0))
        print(f"Current Production accuracy: {prod_acc:.4f}")
    except:
        prod_acc = 0
        print("No existing Production model found.")

    if best_acc > prod_acc:
        print("Registering and promoting best model to Production...")
        promote_best_model(best_run_id, best_acc, model_name, client)
    else:
        print("Best model not better than Production — skipping promotion.")

if __name__ == "__main__":
    train_model_main()