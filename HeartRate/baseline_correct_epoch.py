import neurokit2 as nk
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# Define Subject IDs and Runs
# ------------------------------
IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
       "68", "69", "70", "72", "73", "74"]
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ------------------------------
# Define Directories
# ------------------------------
outdir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/neurokit/"

# ------------------------------
# Define Flanker Start Event Codes (NEW)
# ------------------------------
flanker_start_events = [3, 7, 11, 15]  # Only these events will be used for epoching

# ------------------------------
# Loop Through Each Subject and Run
# ------------------------------
for ID in IDs:
    for run in runs:
        try:
            run = str(run)
            fn = f"/Users/nadezhdabarbashova/Desktop/fmcc_timing/HR/{ID}_run{run}.txt"
            print(f"Processing: {fn}")

            # ------------------------------
            # Step 1: Load Data
            # ------------------------------
            data = pd.read_csv(fn, sep="\t", header=None)
            data.columns = ["timepoint", "ECG", "EVENT"]

            # ------------------------------
            # Step 2: Clean ECG Data
            # ------------------------------
            data["ECG_Cleaned"] = nk.ecg_clean(data["ECG"], sampling_rate=100)

            # ------------------------------
            # Step 3: Process ECG (Detect Peaks, HR)
            # ------------------------------
            signals, infoECG = nk.ecg_process(data["ECG_Cleaned"], sampling_rate=100)

            # ------------------------------
            # Step 4: Merge Processed ECG Data with Original Data
            # ------------------------------
            data = pd.concat([data, signals], axis=1)

            # ------------------------------
            # Step 5: Identify Flanker Start Events (NEW)
            # ------------------------------
            flanker_events_df = data[data["EVENT"].isin(flanker_start_events)]  # Select only flanker start events
            event_indices = flanker_events_df.index.tolist()  # Get indices of flanker events

            # ------------------------------
            # Step 6: Convert Event Indices to Time (NEW)
            # ------------------------------
            sampling_rate = 100  # Adjust based on actual data
            event_timestamps = [idx / sampling_rate for idx in event_indices]  # Convert index to seconds

            # ------------------------------
            # Step 7: Create a DataFrame for Selected Events (NEW)
            # ------------------------------
            events_df = pd.DataFrame({
                "onset": event_timestamps,
                "condition": flanker_events_df["EVENT"].values
            })

            # ------------------------------
            # Step 8: Create 30-Second Epochs for Flanker Start Events (NEW)
            # ------------------------------
            epochs = nk.epochs_create(
                data=data,
                events=event_indices,  # Use only flanker start event indices
                sampling_rate=sampling_rate,
                epochs_start=0,  # Start at event onset
                epochs_end=30,  # Capture 30 seconds after the event
                event_labels=events_df["condition"].tolist(),
                baseline_correction=True  # Normalize using baseline correction
            )

            # ------------------------------
            # Step 9: Save Each Epoch Separately (NEW)
            # ------------------------------
            for event_label, epoch_df in epochs.items():
                epoch_filename = os.path.join(outdir, f"{ID}_EKG_epoch_FlankerStart_{event_label}_run{run}.csv")
                epoch_df.to_csv(epoch_filename, index=False)
                print(f"Saved epoch: {epoch_filename}")

            # ------------------------------
            # Step 10: Save Full Processed Dataset
            # ------------------------------
            save_filename = os.path.join(outdir, f"{ID}_EKG_ECode_HeartRate{run}.csv")
            data.to_csv(save_filename, index=False)
            print(f"Saved processed data: {save_filename}")

        except Exception as e:
            print(f"Error processing {ID} Run {run}: {e}")
