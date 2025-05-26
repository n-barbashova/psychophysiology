import os
import pandas as pd
import numpy as np

# this script goes through and saves the data as timing files (for LedaLab) just like my other EDA file. 
# This one however labels only the countdown end events (proximal stim end, proximal shock end, distal stim end, distal shock end)
# This way I can look at the whole countdown (60 seconds, or 15 seconds leading up to the end code to better see this)
# This is in contrast to my other script which filters out end codes nad keeps start events (countdown start and flanker start, etc)
# each event code needs to have one row (remove repeat rows) - this is important for LedaLab! 

# Directories
rawdata = "/Users/nadezhdabarbashova/Documents/fmcc_heart_rate/raw_csv"
save_dir = "/Users/nadezhdabarbashova/Documents/fmcc_EDA/timing_files_end_codes/"

# Subjects and runs
IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
       "68", "69", "70", "72", "73", "74", "76", "78", "81", "82", "84", "85", "87",
       "88", "89", "91", "93", "98", "99", "100", "104", "107", "109", "110"]
runs = list(range(9))

# Countdown end event codes
countdown_end_codes = {2, 6, 10, 14}

for ID in IDs:
    for run in runs:
        current_dir = os.path.join(rawdata, f"sub{ID}")
        current_file = f"fmcc_sub{ID}_task_000{run}.csv"
        path = os.path.join(current_dir, current_file)

        try:
            tmp_df = pd.read_csv(path, header=None, delimiter=',')
        except Exception as e:
            print(f"❌ Error reading file {path}: {e}")
            continue

        data = tmp_df.drop(index=0).drop(columns=[2]).reset_index(drop=True)
        data.columns = ['EDA', 'ECG', 'Stim', 'ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7']

        # Label only countdown end events
        event_conditions = [
            # Distal shock countdown end → 2
            ((data['ch0'] == 5) & (data['ch1'] == 5) & (data['ch2'] == 0) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),
            # Proximal shock countdown end → 6
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 5) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),
            # Distal stim countdown end → 10
            ((data['ch0'] == 0) & (data['ch1'] == 5) & (data['ch2'] == 5) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),
            # Proximal stim countdown end → 14
            ((data['ch0'] == 5) & (data['ch1'] == 5) & (data['ch2'] == 5) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0))
        ]
        condition_values = [2, 6, 10, 14]
 
        # Assign only countdown ends, label everything else as 0
        data['EVENT'] = np.select(event_conditions, condition_values, default=0)
        
        # Downsample to 100Hz (every 20th row from 2000Hz)
        data_save = data[['EDA', 'EVENT']][::20].copy().reset_index(drop=True)
        data_save['timepoint'] = 0.01 * data_save.index

        # Define event labels for interpretation
        event_labels = {
            2: "Distal shock end",
            6: "Proximal shock end",
            10: "Distal stim end",
            14: "Proximal stim end"
        }

       
         # Track last seen event codes and their row indices
        recent_events = {}

        # Define window size (59 seconds)
        window_size = 6000

        for k in range(len(data_save)):
            event_code = data_save.loc[k, 'EVENT']

            if event_code > 0:  # Only check nonzero event codes
                # Check if this event has appeared in the last 3000 rows
                if event_code in recent_events and (k - recent_events[event_code] < window_size):
                    data_save.loc[k, 'EVENT'] = 0  # Set duplicate event to 0
                else:
                    recent_events[event_code] = k  # Store latest occurrence
    
        
        data_save = data_save[['timepoint', 'EDA', 'EVENT']]

        # Extract the order of event codes as they appear - check what order things are in 
        ordered_events = data_save[data_save['EVENT'] > 0]['EVENT'].tolist()

        if ordered_events:
            print("   → Event order:")
            for idx, code in enumerate(ordered_events):
                label = event_labels.get(code, "Unknown")
                print(f"     {idx+1}. Code {code}: {label}")
        else:
            print("   → No countdown end events retained.")
        
        num_events = (data_save['EVENT'] > 0).sum()
        print(f"{ID} run {run + 1}: {num_events} event(s) retained")
        code_counts = data_save['EVENT'].value_counts().sort_index()
        for code, count in code_counts.items():
            if code > 0:
                print(f"   → Event code {code}: {count} time(s)")


        # ✅ Save all rows (only countdown end codes will be non-zero)
        savefile = f"{ID}_run{run + 1}_countdown_endonly.txt"
        save_path = os.path.join(save_dir, savefile)
        data_save.to_csv(save_path, header=None, index=None, sep='\t')

        print(f"✅ Saved countdown-end timing file: {save_path}")
