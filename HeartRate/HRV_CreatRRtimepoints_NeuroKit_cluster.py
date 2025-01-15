# Load NeuroKit and other useful packages
import neurokit2 as nk
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt

IDs = ["006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "035", "036", "037", "038", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052", "053", "054", "055", "056", "057", "059", "060", "062", "063", "064", "065", "066", "067", "068", "069"]
runs = ["1", "2", "3", "4", "5", "6"]
outdir = "/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/EKG_processed"
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
remove_txt_files_in_folder(outdir)
for ID in IDs:
    for run in runs:
        try:
            #Load data
            fn = "/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/EKG_processed/" + ID + "_encodingEKG_"+ run + ".txt"
            data = pd.read_csv(fn, sep="\t", header=None)
            data.columns = ["timepoint", "EKG", "EventCode"]

            #Clean data
            data_cleaned = nk.ecg_clean(data["EKG"], sampling_rate=100)
            # Get heart rate
            signals, infoECG = nk.ecg_process(data_cleaned, sampling_rate=100)

            # Merge signals and data info
            datasignal = pd.concat([signals, data], axis=1)
            # save
            # Save the current dataframe
            save = ID + "_encodingEKG_ECode_HeartRate" + run + ".csv"
            datasignal.to_csv(os.path.join(outdir, save), index=None, sep=',')

            # Find peaks
            peaks, info = nk.ecg_peaks(data_cleaned, sampling_rate=100, correct_artifacts=True)

            #Find Event Code indexes
            EventCode_idx = np.array(data.loc[data['EventCode']>0].index)

            #Find R peak timepoints
            R = data.loc[info["ECG_R_Peaks"]]["timepoint"].to_list()

            #Get the R-R interval and convert to ms.
            # RR = np.diff(info["ECG_R_Peaks"])*10

            #Get event code list with define event code occurance in between peaks.
            EventCode = []
            EventCodeTimePoint = []
            #Find the event code and event code timepoint that near the R peak
            j = 1
            for i in range(len(info["ECG_R_Peaks"])):
                #Try to find Event Code
                if np.isin(info["ECG_R_Peaks"][i], EventCode_idx):
                    tmpEventCode = data.loc[info["ECG_R_Peaks"][i], 'EventCode']
                    tmpEventCodeTimePoint = data.loc[info["ECG_R_Peaks"][i], 'timepoint']
                    EventCode.append(tmpEventCode)
                    EventCodeTimePoint.append(tmpEventCodeTimePoint)
                # Find event code that is within 2s of a R peak
                elif np.any((EventCode_idx >= (info["ECG_R_Peaks"][i] - 150)) & (EventCode_idx <= (info["ECG_R_Peaks"][i] + 150))):
                    tmpEventCodeidx = EventCode_idx[(EventCode_idx >= (info["ECG_R_Peaks"][i] - 150)) & (EventCode_idx <= (info["ECG_R_Peaks"][i] + 150))][0]
                    tmpEventCode = data.loc[tmpEventCodeidx, 'EventCode']
                    tmpEventCodeTimePoint = data.loc[tmpEventCodeidx, 'timepoint']
                    EventCode.append(tmpEventCode)
                    EventCodeTimePoint.append(tmpEventCodeTimePoint)
                else:
                    EventCode.append(0)
                    EventCodeTimePoint.append(info["ECG_R_Peaks"][i])


            #Make a dataframe and save
            df = pd.DataFrame({"R": R, "EventCode": EventCode, "EventCodeTimePoint" : EventCodeTimePoint})
            # remove event code when appeared twice in the same trial
            indexli = []
            for k in range(len(df)):
                if k < len(df) - 1:
                    Code1 = df.loc[k]['EventCode']
                    Code2 = df.loc[k+1]['EventCode']
                    if Code1>0 and Code2>0:
                        indexli.append(k+1)
            for ind in indexli:
                df.loc[ind, "EventCode"] = 0
            #Add the TrialNum column
            df['TrialNum'] = df['EventCode']
            mask1=df['TrialNum'].apply(lambda x: 1 if x > 0 else 0).astype('bool')
            list1 = list(range(1, 33))
            df.loc[mask1, 'TrialNum'] = list1

            save = ID + "_encodingEKG_ECode_" + run + ".csv"
            df.to_csv(os.path.join(outdir,save), header=None, index=None, sep=',')
        except:
            print("Cannot load: ID: " + ID + " run: " + run)


        # hrv = nk.hrv_time(peaks, sampling_rate=100, show=True)
        # hrv_indices = nk.hrv(peaks, sampling_rate=100, show=True)
        # hrv_indices
        # print("here")