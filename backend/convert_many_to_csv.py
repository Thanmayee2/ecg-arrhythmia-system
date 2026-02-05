import wfdb
import pandas as pd
import os
import pandas as pd

# Path where PTB-XL dataset exists
BASE_PATH = r"C:\Users\HP\Downloads\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3"

# Metadata CSV
meta_path = os.path.join(BASE_PATH, "ptbxl_database.csv")

# Load metadata
meta = pd.read_csv(meta_path)

# Folder to save CSV files
output_dir = r"C:\Users\HP\Downloads\ECG_Arrhythmia_Project\backend\csv_output"
os.makedirs(output_dir, exist_ok=True)

# Take first 10 records
records = meta["filename_lr"].head(10)

print("Converting 10 ECG records...")

for i, rec in enumerate(records):
    try:
        record_path = os.path.join(BASE_PATH, rec)

        record = wfdb.rdrecord(record_path)

        # Convert signals to dataframe
        df = pd.DataFrame(record.p_signal)

        # Save CSV
        out_file = os.path.join(output_dir, f"ecg_{i}.csv")
        df.to_csv(out_file, index=False, header=False)

        print(f"Saved: {out_file}")

    except Exception as e:
        print("Error:", rec, e)

print("Done converting files.")
