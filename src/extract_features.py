import os
import pandas as pd
import numpy as np

# Update to match your folder structure
BASE_DIR = "/opt/flows/predictive_maintenance_project/data/raw/Nasa-Bearing"
TEST_SETS = ["1st_test", "2nd_test", "3rd_test"]
OUTPUT_FILE = "/opt/flows/predictive_maintenance_project/data/processed/features.csv"

def extract_features_from_file(filepath):
    df = pd.read_csv(filepath, sep=r"\s+", header=None)
    features = {}
    for col in df.columns:
        signal = df[col]
        features[f"mean_{col}"] = signal.mean()
        features[f"rms_{col}"] = np.sqrt(np.mean(signal**2))
        features[f"std_{col}"] = signal.std()
        features[f"kurtosis_{col}"] = signal.kurtosis()
        features[f"skew_{col}"] = signal.skew()
        features[f"peak_{col}"] = signal.max()
    return features

def  extract_features_main():
    feature_rows = []
    for test_set in TEST_SETS:
        folder_path = os.path.join(BASE_DIR, test_set, test_set)
        files = sorted(os.listdir(folder_path))
        for fname in files:
            path = os.path.join(folder_path, fname)
            if not os.path.isfile(path):
                continue
            try:
                features = extract_features_from_file(path)
                features["filename"] = fname
                features["source"] = test_set
                feature_rows.append(features)
            except Exception as e:
                print(f"Skipped file {fname} due to error: {e}")

    features_df = pd.DataFrame(feature_rows)

    # Label last 10% of files in each set as "failure"
    features_df["label"] = 0
    for test_set in TEST_SETS:
        idx = features_df[features_df["source"] == test_set].index
        cutoff = int(len(idx) * 0.9)
        failure_idx = idx[cutoff:]
        features_df.loc[failure_idx, "label"] = 1

    features_df.to_csv(OUTPUT_FILE, index=False)
    print(f" Saved features for {len(features_df)} files → {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_features_main()
