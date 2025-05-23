
import neurokit2 as nk
import os
import pandas as pd
import numpy as np


IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
         "68", "69", "70", "72", "73", "74"]

IDs = ["76", "78", "81", "82", "84", "85", "86", "87",
           "88", "89", "91", "93", "98", "99", "100", "103",
            "104"]

# peaks - r peak is the big peak, the important one
#IDs = [49]
runs = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]

outdir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/neurokit/"


for ID in IDs:
    for run in runs:
        try:
            run = str(run)
            fn = f"/Users/nadezhdabarbashova/Desktop/fmcc_timing/neurokit/{ID}_EKG_ECode_HeartRate{run}.csv"
            print(f"Processing: {fn}")

            data = pd.read_csv(fn)
            data['event_chunk_countdown'] = 0
            data['event_chunk_flanker'] = 0
            data['threat_type'] = ""
            data['distance_type'] = ""
            data['event_type'] = ""

            event_pairs_countdown = [(1, 2), (5, 6), (9, 10), (13, 14)]
            event_pairs_flanker = [(3, 4), (7, 8), (11, 12), (15, 16)]
            # If EVENT is an end code, assign the correct event_type
            data.loc[data['EVENT'] == 2, 'event_type'] = 'distal shock countdown end'
            data.loc[data['EVENT'] == 6, 'event_type'] = 'proximal shock countdown end'
            data.loc[data['EVENT'] == 10, 'event_type'] = 'distal stim countdown end'
            data.loc[data['EVENT'] == 14, 'event_type'] = 'proximal stim countdown end'

            print("checl ends codes")
            print(data[data['event_type'].notna() & data['event_type'].str.contains("end")])

            for start, end in event_pairs_countdown:
                if (data['EVENT'] == start).any() and (data['EVENT'] == end).any():
                    start_idx = data.index[data['EVENT'] == start][0]
                    end_idx = data.index[data['EVENT'] == end][0]
                    mask = (data.index >= start_idx) & (data.index <= end_idx + 1)  # Inclusive
                    data.loc[mask, 'event_chunk_countdown'] = start
            for start, end in event_pairs_flanker:
                if (data['EVENT'] == start).any() and (data['EVENT'] == end).any():
                    start_idx = data.index[data['EVENT'] == start][0]
                    end_idx = data.index[data['EVENT'] == end][0]
                    mask = (data.index >= start_idx) & (data.index <= end_idx)  # Inclusive
                    data.loc[mask, 'event_chunk_flanker'] = start


            # yikes
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

            ### add end codes
            print("check ends codes AGAIN")
            print(data[data['event_type'].notna() & data['event_type'].str.contains("end")])

            ## count every instance of event code.
            end_event_types = [
                'distal shock countdown end',
                'proximal shock countdown end',
                'distal stim countdown end',
                'proximal stim countdown end'
            ]

            # Initialize tracking variables
            interval_counter = 0
            last_seen = {event: -3000 for event in end_event_types}  # Track last occurrence index
            check_rows = 3000

            # Add a new column to store interval numbers
            data["intervalNum"] = 0

            for idx, row in data.iterrows():
                event = row['event_type']
                if event in end_event_types:
                    # Ensure it's the first instance in a batch (not preceded by the same event)
                    if idx == 0 or data.at[idx - 1, 'event_type'] != event:
                        # Ensure it wasn't seen in the last `check_rows`
                        if idx - last_seen[event] > check_rows:
                            interval_counter += 1
                            last_seen[event] = idx  # Update last seen index

                            # Store the interval count in the new column
                            data.at[idx, 'intervalNum'] = interval_counter

            ## fill up

            # Display the modified dataframe

            # **Filter: Keep only rows where event_type is NOT empty and NOT NA**
            data_filtered = data[data['event_type'].notna() & (data['event_type'] != "")]
            #print(f"After filtering: {data_filtered.shape[0]} rows remaining")

            print(data["intervalNum"].unique())  # See what values exist
            data.loc[data["intervalNum"] == 0, "intervalNum"] = pd.NA

            data["intervalNum"] = data["intervalNum"].ffill()
            # Ensure it's still an integer column
            data["intervalNum"] = data["intervalNum"].astype("Int64")
            print(data["intervalNum"].unique())  # See what values exist

            # Fill any remaining NaNs (if first rows were empty) with the first valid value
            if data["intervalNum"].isna().sum() > 0:
                first_valid_index = data["intervalNum"].first_valid_index()
                if first_valid_index is not None:
                    data.loc[:first_valid_index, "intervalNum"] = data.loc[first_valid_index, "intervalNum"]
            print(data["intervalNum"].unique())  # See what values exist

            # **Downsample: Keep every 10th row**
            data_downsampled = data_filtered

            #data_downsampled = data_filtered.iloc[::10, :]
            #print(f"After downsampling: {data_downsampled.shape[0]} rows remaining")

            # **Save the processed dataframe**
            save_csv = os.path.join(outdir, f"{ID}_EKG_events_run{run}.csv")
            data_downsampled.to_csv(save_csv, index=False, sep=',')
            print(f"Saved: {save_csv}")


        except Exception as e:
            print(f"Cannot load: ID: {ID}, run: {run}. Error: {e}")




