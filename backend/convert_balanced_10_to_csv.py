import os
import ast
import wfdb
import pandas as pd

BASE_PATH = r"C:\Users\HP\Downloads\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3"
meta_path = os.path.join(BASE_PATH, "ptbxl_database.csv")

output_dir = r"C:\Users\HP\Downloads\ECG_Arrhythmia_Project\backend\csv_output"
os.makedirs(output_dir, exist_ok=True)

meta = pd.read_csv(meta_path)

# Extract main label
meta["scp_codes"] = meta["scp_codes"].apply(ast.literal_eval)
meta["label"] = meta["scp_codes"].apply(lambda d: list(d.keys())[0] if len(d) else "UNKNOWN")

# Choose labels you trained on
target_labels = ["NORM", "IMI", "ASMI", "LVH", "NDT"]

# Pick 2 records per label = 10 total
selected_rows = []
for lab in target_labels:
    rows = meta[meta["label"] == lab].head(2)
    selected_rows.append(rows)

selected = pd.concat(selected_rows).reset_index(drop=True)

print("Selected labels count:")
print(selected["label"].value_counts())

for i, row in selected.iterrows():
    rec = row["filename_lr"]
    label = row["label"]

    try:
        record_path = os.path.join(BASE_PATH, rec)
        record = wfdb.rdrecord(record_path)

        df = pd.DataFrame(record.p_signal)

        out_file = os.path.join(output_dir, f"{label}_{i}.csv")
        df.to_csv(out_file, index=False, header=False)

        print("Saved:", out_file)

    except Exception as e:
        print("Error converting", rec, e)

print("Done.")
