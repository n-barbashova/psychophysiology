# Load NeuroKit and other useful packages
import neurokit2 as nk
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
       #   "68", "69", "70", "72", "73", "74"]

# peaks - r peak is the big peak, the imporant one

IDs = [49]

IDs = ["76", "78", "81", "82", "84", "85", "86", "87",
           "88", "89", "91", "93", "98", "99", "100", "103",
            "104"]

runs = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]


outdir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/neurokit/"

# plot the heart rate
figs_dir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/HR/figs/"


# for ID in IDs:
#     for run in runs:
#         try:
#             run = str(run)
#             fn = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/HR/" + ID + "_run" + run + ".txt"
#             print(f"Processing: {fn}")
#
#             # Load data
#             data = pd.read_csv(fn, sep="\t", header=None)
#             data.columns = ["timepoint", "ECG", "EVENT"]
#
#             # Clean ECG data
#             data_cleaned = nk.ecg_clean(data["ECG"], sampling_rate=100)
#
#             # Plot ECG Signal
#             plt.figure(figsize=(100, 6))
#             plt.plot(data["timepoint"], data_cleaned, label="ECG Signal", color="blue", linewidth=1)
#             plt.xlabel("Time (ms)")
#             plt.ylabel("ECG Amplitude")
#             plt.title(f"Heart Rate Signal - {ID} Run {run}")
#             plt.legend()
#             plt.grid(True)
#
#             # Save the figure
#             save_path = os.path.join(figs_dir, f"{ID}_HR_plot_run{run}.png")
#             plt.savefig(save_path, dpi=300, bbox_inches="tight")
#             plt.close()
#
#             print(f"Saved plot: {save_path}")
#
#         except Exception as e:
#             print(f"Error processing {ID} Run {run}: {e}")



# fn = "/Users/nadezhdabarbashova/Library/CloudStorage/Dropbox/LEAP_Neuro_Lab/researchProjects/nadu/fmcc/pipeline_psychopyz_nadu/HeartRate/HR/49_run1.txt"
# data = pd.read_csv(fn, sep="\t", header=None)

def remove_txt_files_in_folder(folder_path):
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path) and file_name.endswith('.csv'):
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            else:
                print(f"Skipping {file_path}. It's either not a file or not a .csv file.")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
#Remove all the txt files from EKG processed folder

# remove_txt_files_in_folder(outdir)

for ID in IDs:
    for run in runs:
        try:
            #Load data
            run = str(run)
            fn = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/HR/" + ID + "_run"+ run + ".txt"
            #fn = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/HR/49_run1.txt"
            print(fn)
            # something gores wrong here - this line
            data = pd.read_csv(fn, sep="\t", header=None)
            print(data.head())  # Print the first few rows to verify the output
            print("data loaded")
            data.columns = ["timepoint", "ECG", "EVENT"]
            #Clean data - nk package smooths the data - downsample 100
            data_cleaned = nk.ecg_clean(data["ECG"], sampling_rate=100)


            # Get heart rate - find peaks
            signals, infoECG = nk.ecg_process(data_cleaned, sampling_rate=100)
            # nk.signal_plot(ecg_cleaned)
            print("signals and infoECG collected")


            # Merge signals and data info - use peaks
            datasignal = pd.concat([signals, data], axis=1)
            # save
            # Save the current dataframe
            save = ID + "_EKG_ECode_HeartRate" + run + ".csv"
            datasignal.to_csv(os.path.join(outdir, save), index=None, sep=',')
            print("data saved")

            # Find peaks
            peaks, info = nk.ecg_peaks(data_cleaned, sampling_rate=100, correct_artifacts=True)

            # merge new cols
            peaks["timepoint"] = data["timepoint"]  # Add time column
            peaks["EVENT"] = data["EVENT"]  # Retain Event Code
            print("Peaks:")
            print(peaks.head())

            hrv_indices = nk.hrv(peaks, sampling_rate=100, show=True)
            print("hrv_indices:")
            print(hrv_indices.head())

            peak_fn = os.path.join(outdir, f"hrv_indices{ID}_run{run}.csv")  # Use .csv instead of .txt for saving a DataFrame
            hrv_indices.to_csv(peak_fn, index=False)
            print(f"HRV indices saved to: {peak_fn}")

            ## it gets this far 
            #Find Event Code indexes
            EventCode_idx = np.array(data.loc[data['EventCode']>0].index)

            #Find R peak timepoints
            R = data.loc[info["ECG_R_Peaks"]]["timepoint"].to_list()

            # Step 5: Identify Flanker Start Events (NEW)
            # ------------------------------
            flanker_events_df = data[data["EVENT"].isin(flanker_start_events)]  # Select only flanker start events
            event_indices = flanker_events_df.index.tolist()  # Get indices of flanker events

            # ------------------------------
            # Step 6: Convert Event Indices to Time (NEW)
            # ------------------------------
            print("step 6")

            sampling_rate = 100  # Adjust based on actual data
            event_timestamps = [idx / sampling_rate for idx in event_indices]  # Convert index to seconds

            # ------------------------------
            # Step 7: Create a DataFrame for Selected Events (NEW)
            # ------------------------------
            print("step 7")
            events_df = pd.DataFrame({
                "onset": event_timestamps,
                "condition": flanker_events_df["EVENT"].values
            })

            # ------------------------------
            # Step 8: Create 30-Second Epochs for Flanker Start Events (NEW)
            # ------------------------------
            print("step 8")

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

            # Get the R-R interval and convert to ms.
            # RR = np.diff(info["ECG_R_Peaks"])*10

            #Get event code list with define event code occurance in between peaks.
            EventCode = []
            EventCodeTimePoint = []
            #Find the event code and event code timepoint that near the R peak
            j = 1
            for i in range(len(info["ECG_R_Peaks"])):
                #Try to find Event Code
                if np.isin(info["ECG_R_Peaks"][i], EventCode_idx):
                    tmpEventCode = data.loc[info["ECG_R_Peaks"][i], 'EVENT']
                    tmpEventCodeTimePoint = data.loc[info["EC_R_Peaks"][i], 'timepoint']
                    EventCode.append(tmpEventCode)
                    EventCodeTimePoint.append(tmpEventCodeTimePoint)
                # Find event code that is within 2s of a R peak
                elif np.any((EventCode_idx >= (info["ECG_R_Peaks"][i] - 150)) & (EventCode_idx <= (info["ECG_R_Peaks"][i] + 150))):
                    tmpEventCodeidx = EventCode_idx[(EventCode_idx >= (info["ECG_R_Peaks"][i] - 150)) & (EventCode_idx <= (info["ECG_R_Peaks"][i] + 150))][0]
                    tmpEventCode = data.loc[tmpEventCodeidx, 'EVENT']
                    tmpEventCodeTimePoint = data.loc[tmpEventCodeidx, 'timepoint']
                    EventCode.append(tmpEventCode)
                    EventCodeTimePoint.append(tmpEventCodeTimePoint)
                else:
                    EventCode.append(0)
                    EventCodeTimePoint.append(info["ECG_R_Peaks"][i])



            #Make a dataframe and save
            #df = pd.DataFrame({"R": R, "EventCode": EventCode, "EventCodeTimePoint" : EventCodeTimePoint})


        except:
            print("Part of the loop was not completed: " + ID + " run: " + run)

        #hrv_indices
        print("here")
