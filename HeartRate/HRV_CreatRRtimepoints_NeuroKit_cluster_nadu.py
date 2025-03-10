# Load NeuroKit and other useful packages
import neurokit2 as nk
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
         "68", "69", "70", "72", "73", "74"]

# peaks - r peak is the big peak, the imporant one

#IDs = [49]
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

            # try to merge new cols
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

            #Find Event Code indexes
            EventCode_idx = np.array(data.loc[data['EventCode']>0].index)

            #Find R peak timepoints
            R = data.loc[info["ECG_R_Peaks"]]["timepoint"].to_list()

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
            df = pd.DataFrame({"R": R, "EventCode": EventCode, "EventCodeTimePoint" : EventCodeTimePoint})

            # remove event code when appeared twice in the same trial

            # indexli = []
            # for k in range(len(df)):
            #     if k < len(df) - 1:
            #         Code1 = df.loc[k]['EventCode']
            #         Code2 = df.loc[k+1]['EventCode']
            #         if Code1>0 and Code2>0:
            #             indexli.append(k+1)
            # for ind in indexli:
            #     df.loc[ind, "EventCode"] = 0
            # #Add the TrialNum column
            # df['TrialNum'] = df['EventCode']
            # mask1=df['TrialNum'].apply(lambda x: 1 if x > 0 else 0).astype('bool')
            # list1 = list(range(1, 33))
            # df.loc[mask1, 'TrialNum'] = list1

            #save = ID + "_encodingEKG_ECode_" + run + ".csv"
            #df.to_csv(os.path.join(outdir, save), header=None, index=None, sep=',')

        except:
            print("Part of the loop was not completed: " + ID + " run: " + run)

        #hrv_indices
        print("here")
