# Script for collapsing across digital channels

import pandas as pd
import os
import numpy as np

# To do:
# import this quarter's task file
# recalculate the 60 seconds - check it
# check it against one subject's data and see if it matches up with the order of the countdowns

# the timing files we want to get are three columns  - timestamp,  event code, event name
# import csv that you created, select the EDA column (& HR)

# we have to downsample at the end so that there is only one row with an event code per event code
# start has one row, end has one row - LedaLab needs to have just one row AND alos LedaLab can't handle
# high sampling rate

#####  INPUT DIRECTORY
#raw data - the data should already be in csv format. Each row represents a sample (2000 per second)
# rawdata = "/Users/nadezhdabarbashova/Library/CloudStorage/Dropbox/LEAP_Neuro_Lab/researchProjects/nadu/fmcc/data/fmcc_w25/fmcc_csv"

rawdata = "/Users/nadezhdabarbashova/Documents/fmcc_heart_rate/raw_csv"

#####  OUTPUT DIRECTORY
#save directory - processed event code timing files go here
# save_dir = "/Users/nadezhdabarbashova/Library/CloudStorage/Dropbox/LEAP_Neuro_Lab/researchProjects/nadu/fmcc/data/fmcc_w25/acq_data/timing/"
 
save_dir = "/Users/nadezhdabarbashova/Documents/fmcc_EDA/timing_files/"

IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
           "68", "69", "70", "72", "73", "74", "76", "78", "81", "82", "84", "85", "87",
           "88", "89", "91", "93", "98", "99", "100", "104", "107", "109", "110"]

# We need to record the start event code conditions for runs so that it can be used for the other analysis
subject = []
runli = []
startcode = []
runs = [0, 1, 2, 3, 4, 5, 6, 7, 8]



# Define a function that find the index of not none elements in the list
# this will be used later - all channels that don't have an event will be given "none"
def find_non_none_indices(lst):
    indices = [i for i, element in enumerate(lst) if element != 'none']
    return indices

# run 3

# loop through each participant, then each run
for ID in IDs:
    for run in runs:
        print("Starting run num:", run)
        subject.append(ID) #subject list
        runli.append(run)  #run list - in the end you have info to make a spreadsheet
        # construct the sub directory where the input is located for each subject 
        current_dir = rawdata + "/" + "sub" + str(ID) 

        # construct the file name for each subject and each run 
        current_file = "fmcc_sub" + ID + "_task_000" + str(run) + ".csv"
        
        # combine into a full path and read the path 
        path = os.path.join(current_dir, current_file)

        # create a temporary df to start with
        tmp_df = pd.read_csv(path, header=None, delimiter=',')  # your txt or csv file from acqknowledge
        print("Opening file:",current_file )

        # Current columns = EDA, CORR, ECG, Feedback, Stim, ch1-8
        # Let's remove the Corr & Feedback columns
        print(f"Number of columns: {len(tmp_df.columns)}")

        data = (tmp_df  # make a copy of the df and...
                .drop(index=0)  # remove the first row
                .drop(columns=[2])  # drop col2 (0,1,2 - the 3rd channel) - (Feedback channel)
                .reset_index(drop=True))  # reset row index
        #data.head() # see first few rows
        #print(data)  # take a look at the original data
        print(f"Number of columns: {len(data.columns)}")

        # renaming the channels from 0 - 7 instead of 1 - 8 based on Nadu's event code convention
        data.columns = ['EDA', 'ECG', 'Stim', 'ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6',
                        'ch7']

        # add a column and label the events
        # create new column - EVENT - fill it with values - flanker start, flanker end, countdown end
        #### ok problem is that data (whole df) is used here. maybe move it up? label everything, then cut it up,

        print("data shape before creating conditions:")
        print(data.shape)
        #print(data.head())

        event_conditions = [

            ###     Distal shock  ###
            # Distal shock countdown start -  channel: 0, 4, 6
            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Distal shock countdown end - channel: 0, 1, 3, 4, 6   *** fixed
            ((data['ch0'] == 5) & (data['ch1'] == 5) & (data['ch2'] == 0) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Distal shock flanker start - channel: 2
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 5) & (data['ch3'] == 0) &
             (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 0) & (data['ch7'] == 0)),

            # Distal shock flanker end - channels: 0, 2
            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 5) & (data['ch3'] == 0) &
             (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 0) & (data['ch7'] == 0)),

            ###     proximal shock  ###
            # Proximal shock countdown start - channel: 1, 4, 6  -
            ((data['ch0'] == 0) & (data['ch1'] == 5) & (data['ch2'] == 0) & (data['ch3'] == 0) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Proximal shock countdown end - channels: 2, 3, 4, 6  *** fixed
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 5) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Proximal shock flanker start - channel: 3 -
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 5) &
             (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 0) & (data['ch7'] == 0)),

            # Proximal shock flanker end -  channels: 0, 3
            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 5) &
             (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 0) & (data['ch7'] == 0)),

            ###     Distal stim   ###
            # Distal stim countdown start  - channels: 2, 4, 6
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 5) & (data['ch3'] == 0) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Distal stim countdown end - channels: 1, 2, 3, 4, 6 ) *** fixed
            ((data['ch0'] == 0) & (data['ch1'] == 5) & (data['ch2'] == 5) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Distal stim flanker start - channel: 5
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) &
             (data['ch4'] == 0) & (data['ch5'] == 5) & (data['ch6'] == 0) & (data['ch7'] == 0)),

            # Distal stim flanker end  - channels: 0, 5
            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) &
             (data['ch4'] == 0) & (data['ch5'] == 5) & (data['ch6'] == 0) & (data['ch7'] == 0)),

            ###     proximal  stim   ###
            # Proximal stim countdown start   - channels: 0, 2, 4, 6
            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 5) & (data['ch3'] == 0) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Proximal stim countdown end - channels: 0, 1, 2, 3, 4, 6
            ((data['ch0'] == 5) & (data['ch1'] == 5) & (data['ch2'] == 5) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Proximal stim flanker start  - channel 6
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) &
             (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0)),

            # Proximal stim flanker end  - channels: 0, 6
            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) &
             (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 5) & (data['ch7'] == 0))
        ]


        ### TO DO: thse have to be numbers - LedaLab needs numbers - remember which number means what - keep it documented
        # example = values = [7, 1, 2, 3, 4, 5, 6]

        # Define corresponding condition labels in the requested format
        condition_values = [
            1, #'distal shock countdown start',  # 1st condition
            2, #'distal shock countdown end',  # 2nd condition
            3, #'distal shock flanker start',  # 3rd condition
            4, #'distal shock flanker end',  # 4th condition

            5, #'proximal shock countdown start',  # 5th condition
            6, #'proximal shock countdown end',  # 6th condition
            7, #'proximal shock flanker start',  # 7th condition
            8, #'proximal shock flanker end',  # 8th condition

            9, #'distal stim countdown start',  # 9th condition
            10, #'distal stim countdown end',  # 10th condition
            11, #'distal stim flanker start',  # 11th condition
            12, #'distal stim flanker end',  # 12th condition

            13, #'proximal stim countdown start',  # 13th condition
            14, #'proximal stim countdown end',  # 14th condition
            15, #'proximal stim flanker start',  # 15th condition
            16, #'proximal stim flanker end'  # 16th condition
        ]

        #print(f"Number of conditions: {len(event_conditions)}")
        #print(f"Number of values: {len(condition_values)}")

        #print("data shape before labelling:")
        #print(data.shape)

        # data['condition'] = np.select(condition_conditions, condition_values, default='none')
        #data['EVENT'] = np.select(event_conditions, condition_values, default='none')

        data['EVENT'] = np.select(event_conditions, condition_values)


        # Did it find the conditions from the event codes? Check that there are values besides none in the event col
        # The line of code below will count how many rows have a value in the row EVENT - it will tell you how many rows for each unique value, including the none value
        # value_counts = data['EVENT'].value_counts()
        # print(value_counts)

        # Get the start of the countdown - this will be the codes for countdown_start
        conditions = [
            ((data['ch0'] == 5) & (data['ch4'] == 5) & (data['ch6'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) & (
                        data['ch3'] == 0) & (data['ch5'] == 0) & (data['ch7'] == 0)),   # distal shock countdown start

            ((data['ch1'] == 5) & (data['ch4'] == 5) & (data['ch6'] == 5) & (data['ch0'] == 0) & (data['ch2'] == 0) & (
                        data['ch3'] == 0) & (data['ch5'] == 0) & (data['ch7'] == 0)),   # proximal shock countdown start

            ((data['ch2'] == 5) & (data['ch4'] == 5) & (data['ch6'] == 5) & (data['ch1'] == 0) & (data['ch0'] == 0) & (
                        data['ch3'] == 0) & (data['ch5'] == 0) & (data['ch7'] == 0)),  # distal stim countdown start

            ((data['ch0'] == 5) & (data['ch2'] == 5) & (data['ch4'] == 5) & (data['ch6'] == 5) & (data['ch1'] == 0) & (
                        data['ch3'] == 0) & (data['ch5'] == 0) & (data['ch7'] == 0)) ]  # proximal stim countdown start

        values = ['start', 'start', 'start', 'start']

        # data is the df that will later be cut up (into data_rest)
        data['start'] = np.select(conditions, values, default="none")
            #              ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 5)& (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 0 ) & (data['ch7'] == 0 )) | #distal shock flanker start
            #              ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 5) & (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 0 ) & (data['ch7'] == 0 )) | #proximal shock flanker start
            #              ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 5) & (data['ch6'] == 0) & (data['ch7'] == 0 )) | #distal stim flanker start
            #              ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 0) & (data['ch6'] == 5 ) & (data['ch7'] == 0 ))  #proximal stim flanker start

        # all we need is eda, event and index
        data_save = data[['EDA', "EVENT"]]
        encoding_downsample = data_save[::20].copy()
        encoding_downsample.reset_index(inplace=True, drop=True)

        # Add timepoint column
        encoding_downsample['timepoint'] = 0.01 * encoding_downsample.index

        # Reorder columns
        encoding_downsample = encoding_downsample[['timepoint', 'EDA', 'EVENT']]

        # Create a unique filename for each dataset
        savefile = f"{ID}_run{run + 1}.txt"

        #savefile = f"{ID}_run{run + 1}_countdown{i}.mat"
        save_path = os.path.join(save_dir, savefile)
        print(save_path)

        indexli = []
        for k in range(1):
            Code1 = encoding_downsample.loc[k, 'EVENT']
            Code2 = encoding_downsample.loc[k + 1, 'EVENT']
            if int(Code1) > 0 and int(Code2) > 0:
                indexli.append(k + 1)

            for ind in indexli:
                encoding_downsample.loc[ind, "EVENT"] = 0

            # remove repeated event codes (ie countdown numbers) - keep only first instance of all event codes besides 0
           # seen_events = set()  # Track seen EVENT codes
            #for k in range(len(encoding_downsample)):
             #   event_code = encoding_downsample.loc[k, 'EVENT']
             #   if event_code > 0:
              #      if event_code in seen_events:
             #           encoding_downsample.loc[k, 'EVENT'] = 0  # Set repeated instances to 0
              #      else:
              #          seen_events.add(event_code)  # Mark as seen

            # Save the processed DataFrame
            #encoding_downsample.to_csv(save_path, header=None, index=None, sep='\t', mode='w')
            #save = os.path.join(save_dir, savefile)
            #print(f"Full file path: {os.path.join(save_dir, savefile)}")

            # Track last seen event codes and their row indices
            recent_events = {}

            # Define window size (59 seconds)
            window_size = 6100

            for k in range(len(encoding_downsample)):
                event_code = encoding_downsample.loc[k, 'EVENT']

                if event_code > 0:  # Only check nonzero event codes
                    # Check if this event has appeared in the last 3000 rows
                    if event_code in recent_events and (k - recent_events[event_code] < window_size):
                        encoding_downsample.loc[k, 'EVENT'] = 0  # Set duplicate event to 0
                    else:
                        recent_events[event_code] = k  # Store latest occurrence


            # remove any flanker start codes that appear at the end of a countdown, withing 5 seconds of an end event code
            # Define the event codes
            flanker_codes = {3, 7, 11, 15}
            end_codes = {2, 6, 10, 14}

            # Get indices where end codes appear
            end_indices = encoding_downsample[encoding_downsample['EVENT'].isin(end_codes)].index

            # Define window size (5 seconds = 500 rows)
            window_size = 500

            # Loop through each end code index
            for end_idx in end_indices:
                # Look back 500 rows (ensuring we don't go out of bounds)
                start_idx = max(0, end_idx - window_size)

                # Find flanker codes within this range and set them to 0
                encoding_downsample.loc[start_idx:end_idx, 'EVENT'] = encoding_downsample.loc[start_idx:end_idx,
                                                                      'EVENT'].apply(
                    lambda x: 0 if x in flanker_codes else x
                )

            # Define the countdown end codes that need to be turned to 0 - remove them to make it easier in LedaLab
            countdown_end_codes = {2, 4, 6, 8, 10, 12, 14, 16}
            # Set EVENT to 0 where it matches any of the countdown end codes
            encoding_downsample.loc[encoding_downsample['EVENT'].isin(countdown_end_codes), 'EVENT'] = 0

            # test_dir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/"
            # # Ensure the test directory exists
            # if not os.path.exists(test_dir):
            #     os.makedirs(test_dir)  # Create the directory if it doesn’t exist

            save = os.path.join(save_dir, savefile)
            print(f"Full file path: {save}")

            # Try saving the file to the test directory
            encoding_downsample.to_csv(save, header=None, index=None, sep='\t', mode='w')

            # Check if the file exists immediately after saving
            if os.path.exists(save):
                print(f"File successfully saved: {save}")
            else:
                print("File was NOT saved successfully.")


