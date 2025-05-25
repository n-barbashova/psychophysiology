
import neurokit2 as nk
import os
import pandas as pd
import numpy as np
from itertools import groupby


IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
         "68", "69", "70", "72", "73", "74"]

# peaks - r peak is the big peak, the important one
IDs = ["88", "89"]
runs = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]

# output directory 
outdir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/neurokit/"

# plot the heart rate
figs_dir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/HR/figs/"


### process timing files (txt files)
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
            #print(data.head())  # Print the first few rows to verify the output
            print("data loaded")
            data.columns = ["timepoint", "ECG", "EVENT"]
            
            # Clean data - nk package smooths the data - downsample 100
            data_cleaned = nk.ecg_clean(data["ECG"], sampling_rate = 100)

            # Get heart rate - find peaks
            signals, infoECG = nk.ecg_process(data_cleaned, sampling_rate = 100)
            
            # nk.signal_plot(ecg_cleaned)
            print("signals and infoECG collected")

            # Merge signals and data info - use peaks
            datasignal = pd.concat([signals, data], axis=1)
 
            # Save the current dataframe
            save = ID + "_EKG_rough_data_" + run + ".csv"
            #datasignal.to_csv(os.path.join(outdir, save), index=None, sep=',')
            #print("Full data with all rows exported as CSV")
            print("starting event code labelling")

            # rename df for next step. just keep it clean. 
            data = datasignal 
            
            # create new columns  
            data['event_chunk_countdown'] = 0
            data['event_chunk_flanker'] = 0
            data['threat_type'] = ""
            data['distance_type'] = ""
            data['event_type'] = ""
            
            # create new columns  pairs - start and end of countdown and start and end of flanker task 
            event_pairs_countdown = [(1, 2), (5, 6), (9, 10), (13, 14)]
            event_pairs_flanker = [(3, 4), (7, 8), (11, 12), (15, 16)]
            
            # If EVENT is an end code, assign the correct event_type
            data.loc[data['EVENT'] == 2, 'event_type'] = 'distal shock countdown end'
            data.loc[data['EVENT'] == 6, 'event_type'] = 'proximal shock countdown end'
            data.loc[data['EVENT'] == 10, 'event_type'] = 'distal stim countdown end'
            data.loc[data['EVENT'] == 14, 'event_type'] = 'proximal stim countdown end'

            print("check end codes")
            print(data[data['event_type'].notna() & data['event_type'].str.contains("end")])

            # check whether both codes in event_pairs_countdown are found in the EVENT column. 
            # find the first row index of each. 
            # create boolean mask for all rows between start and end, inclusive. 

            print("about to convert the event chunk coundown col to object")
            data['event_chunk_countdown'] = data['event_chunk_countdown'].astype("object")


            print("about to label start, end, baseline")
            for start, end in event_pairs_countdown:
                if (data['EVENT'] == start).any() and (data['EVENT'] == end).any():
                    # find the first row index of each. 
                    start_idx = data.index[data['EVENT'] == start][0] # 
                    end_idx = data.index[data['EVENT'] == end][0]
                    # create a mask - greater than start, less than end 
                    mask = (data.index >= start_idx) & (data.index <= end_idx + 1)  # Inclusive
                    data.loc[mask, 'event_chunk_countdown'] = start
                    baseline_start = max(0, start_idx - 100)
                    baseline_mask = (data.index >= baseline_start) & (data.index < start_idx)
                    data.loc[baseline_mask, 'event_type'] = "baseline"
                    data.loc[baseline_mask, 'event_chunk_countdown'] = f"baseline_{start}"

            for start, end in event_pairs_flanker:
                if (data['EVENT'] == start).any() and (data['EVENT'] == end).any():
                    start_idx = data.index[data['EVENT'] == start][0]
                    end_idx = data.index[data['EVENT'] == end][0]
                    mask = (data.index >= start_idx) & (data.index <= end_idx)  # Inclusive
                    data.loc[mask, 'event_chunk_flanker'] = start
       
            # interval_counter = 1
            # data["intervalNum"] = pd.NA  # initialize with NA to fill only relevant chunks

            # for start, end in event_pairs_countdown:
            #     start_indices = data.index[data['EVENT'] == start].tolist()
            #     end_indices = data.index[data['EVENT'] == end].tolist()

            #     # Pair start and end indices in order
            #     for s_idx in start_indices:
            #     # Find the first end index that comes after the current start index
            #         e_idx = next((e for e in end_indices if e > s_idx), None)
            #         if e_idx is not None:
            #         # Mark all rows between start and end with the current interval number
            #             mask = (data.index >= s_idx) & (data.index <= e_idx)
            #             data.loc[mask, "intervalNum"] = interval_counter
            #             interval_counter += 1

            # Now add additional labels. Mark the threat type and temporal distance type in 2 new cols 
            data.loc[data['event_chunk_countdown'] == 1, 'threat_type'] = "shock"
            data.loc[data['event_chunk_countdown'] == 1, 'distance_type'] = "distal"
            data.loc[data['event_chunk_countdown'] == 1, 'event_type'] = "distal shock countdown"
            data.loc[data['event_chunk_flanker'] == 3, 'threat_type'] = "shock"
            data.loc[data['event_chunk_flanker'] == 3, 'distance_type'] = "distal"
            data.loc[data['event_chunk_flanker'] == 3, 'event_type'] = "distal shock flanker"
            data.loc[data['event_chunk_countdown'] == 5, 'threat_type'] = "shock"
            data.loc[data['event_chunk_countdown'] == 5, 'distance_type'] = "proximal"
            data.loc[data['event_chunk_countdown'] == 5, 'event_type'] = "proximal shock countdown"
            data.loc[data['event_chunk_flanker'] == 7, 'threat_type'] = "shock"
            data.loc[data['event_chunk_flanker'] == 7, 'distance_type'] = "proximal"
            data.loc[data['event_chunk_flanker'] == 7, 'event_type'] = "proximal shock flanker"
            data.loc[data['event_chunk_countdown'] == 9, 'threat_type'] = "stim"
            data.loc[data['event_chunk_countdown'] == 9, 'distance_type'] = "distal"
            data.loc[data['event_chunk_countdown'] == 9, 'event_type'] = "distal stim countdown"
            data.loc[data['event_chunk_flanker'] == 11, 'threat_type'] = "stim"
            data.loc[data['event_chunk_flanker'] == 11, 'distance_type'] = "distal"
            data.loc[data['event_chunk_flanker'] == 11, 'event_type'] = "distal stim flanker"
            data.loc[data['event_chunk_countdown'] == 13, 'threat_type'] = "stim"
            data.loc[data['event_chunk_countdown'] == 13, 'distance_type'] = "proximal"
            data.loc[data['event_chunk_countdown'] == 13, 'event_type'] = "proximal stim countdown"
            data.loc[data['event_chunk_flanker'] == 15, 'threat_type'] = "stim"
            data.loc[data['event_chunk_flanker'] == 15, 'distance_type'] = "proximal"
            data.loc[data['event_chunk_flanker'] == 15, 'event_type'] = "proximal stim flanker"
            data.loc[data['EVENT'] == 2, 'event_type'] = 'distal shock countdown end'
            data.loc[data['EVENT'] == 6, 'event_type'] = 'proximal shock countdown end'
            data.loc[data['EVENT'] == 10, 'event_type'] = 'distal stim countdown end'
            data.loc[data['EVENT'] == 14, 'event_type'] = 'proximal stim countdown end'

            ### Check end codes 
            print("check end codes AGAIN")
            print(data[data['event_type'].notna() & data['event_type'].str.contains("end")])

            ## count every instance of event code.
            end_event_types = [
                'distal shock countdown end',
                'proximal shock countdown end',
                'distal stim countdown end',
                'proximal stim countdown end']

            # Initialize tracking variables 
            interval_counter = 0
            # last_seen = {event: -2000 for event in end_event_types}  # Track last occurrence index
            # check_rows = 2000
            
            #Add a new column to store interval numbers
 
            # Initialize tracking variables 
            # interval_counter = 0
            # last_seen = {event: -4000 for event in end_event_types}  # Track last occurrence index
            # check_rows = 4000

            # # Add a new column to store interval numbers
            # data["intervalNum"] = 0

            # for idx, row in data.iterrows():
            #     event = row['event_type']
            #     if event in end_event_types:
            #         # Ensure it's the first instance in a batch (not preceded by the same event)
            #         if idx == 0 or data.at[idx - 1, 'event_type'] != event:
            #             # Ensure it wasn't seen in the last `check_rows`
            #             if idx - last_seen[event] > check_rows:
            #                 interval_counter += 1
            #                 last_seen[event] = idx  # Update last seen index

            #                 # Find the last countdown chunk before this point
            #                 prior_chunk_idx = data.loc[:idx][data["event_chunk_countdown"] != 0].last_valid_index()
            #                 if prior_chunk_idx is not None:
            #                     fill_mask = (data.index >= prior_chunk_idx) & (data.index <= idx)
            #                     data.loc[fill_mask, 'intervalNum'] = interval_counter


            # Initialize interval mapping and counter
            interval_mapping = {}
            interval_counter = 1

            # Create column with missing values
            data["intervalNum"] = pd.NA

            # Go row by row and mark the end event types in order
            for idx, row in data.iterrows():
                event = row['event_type']
                if event in end_event_types:
                    if event not in interval_mapping:
                        interval_mapping[event] = interval_counter
                        interval_counter += 1
                    data.at[idx, 'intervalNum'] = interval_mapping[event]

            # Backward fill the interval number across each chunk
            data["intervalNum"] = data["intervalNum"].fillna(method='bfill')

            # Filter only rows with valid event_type
            data_filtered = data[data['event_type'].notna() & (data['event_type'] != "")].copy()

            # Work on data_filtered, not data
            # data_filtered.loc[data_filtered["intervalNum"] == 0, "intervalNum"] = pd.NA
            # data_filtered["intervalNum"] = data_filtered["intervalNum"].ffill()
            # data_filtered["intervalNum"] = data_filtered["intervalNum"].astype("Int64")
            
            print("Interval numbers:")
            print(data_filtered["intervalNum"].unique())

            # Fill any remaining NaNs in intervalNum if they exist
            if data_filtered["intervalNum"].isna().sum() > 0:
                first_valid_index = data_filtered["intervalNum"].first_valid_index()
                if first_valid_index is not None:
                    data_filtered.loc[:first_valid_index, "intervalNum"] = data_filtered.loc[first_valid_index, "intervalNum"]
            
            print("Interval numbers:")
            print(data_filtered["intervalNum"].unique())


            # ** Downsample: Keep every 10th row**
            print(f"Before downsampling: {data_filtered.shape[0]} rows")
            data_downsampled = data_filtered.iloc[::10, :]
            print(f"After downsampling: {data_downsampled.shape[0]} rows")

            # Define the set of end event codes
            end_event_codes = [2, 6, 10, 14]  # These are the EVENT values for "end" rows
           # Remove rows with those end codes
            data_downsampled = data_downsampled[~data_downsampled["EVENT"].isin(end_event_codes)]
            print(f"After removing end codes: {data_downsampled.shape[0]} rows remaining")
           
           
           ## remove extra rows with countdown (the ones that appear at a start of a countdown - i.e proximal)
            # Get mask for countdown rows
            is_countdown = data_downsampled['event_type'].str.contains("countdown", na=False)

            # Create list to mark which countdown groups are "too short"
            keep_mask = np.ones(len(data_downsampled), dtype=bool)

            # Loop through groups of consecutive rows
            idx_start = 0
            for key, group in groupby(is_countdown):
                group_len = len(list(group))
                idx_end = idx_start + group_len
                if key is True and group_len < 3:
                    keep_mask[idx_start:idx_end] = False  # mark short countdown groups for removal
                idx_start = idx_end

            # Apply the mask to keep only valid rows
            data_downsampled = data_downsampled[keep_mask].reset_index(drop=True)


            # ** Save the processed dataframe**
            save_csv = os.path.join(outdir, f"{ID}_EKG_events_run{run}.csv")
            data_downsampled.to_csv(save_csv, index=False, sep=',')
            print(f"Saved: {save_csv}")


        except Exception as e:
            print(f"Error in processing loop for: {ID}, run: {run}. Error: {e}")




