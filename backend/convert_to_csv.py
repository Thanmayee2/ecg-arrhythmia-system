import wfdb
import pandas as pd
import os

# ==============================
# STEP 1: Give the ECG record path (without .dat or .hea extension)
# ==============================
record_path = r"C:\Users\HP\Downloads\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3\records100\21000\21837_lr"

# ==============================
# STEP 2: Read the ECG record
# ==============================
record = wfdb.rdrecord(record_path)

print("ECG Loaded Successfully!")
print("Signal Shape:", record.p_signal.shape)  # (samples, leads)
print("Leads:", record.sig_name)

# ==============================
# STEP 3: Convert ECG signal into CSV
# ==============================
df = pd.DataFrame(record.p_signal)

# ==============================
# STEP 4: Save CSV in current folder
# ==============================
output_csv = "21837_lr.csv"
df.to_csv("21837_lr_full.csv", index=False, header=False)
print(f"\nCSV saved successfully as: {output_csv}")
print("Saved at:", os.path.abspath(output_csv))
