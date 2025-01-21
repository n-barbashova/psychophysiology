# Script for collapsing across digital channels
import pandas as pd
import os
import numpy as np

# the timing files we want to get are three columns  - timestamp,  event code, event name
# import csv that you created, select the EDA column (& HR)

# we have to downsample at the end so that there is only one row with an event code per event code
# start has one row, end has one row - LedaLab needs to have just one row AND alos LedaLab can't handle
# high sampling rate

#save directory - processed event code timing files go here
save_dir = "/Users/nadezhdabarbashova/Library/CloudStorage/Dropbox/LEAP_Neuro_Lab/researchProjects/nadu/fmcc/data/acq_data/EDA_processed"

#raw data - the data should already be in csv format. Each row represents a sample (2000 per second)
rawdata = "/Users/nadezhdabarbashova/Library/CloudStorage/Dropbox/LEAP_Neuro_Lab/researchProjects/nadu/fmcc/data/acq_data/fmcc_csv"
IDs = ["03"]

# We need to record the start event code conditions for runs so that it can be used for the other analysis
subject = []
runli = []
startcode = []
runs = [3]


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
        current_dir = rawdata + "/" + ID
        current_file = "fmcc_sub" + ID + "_task_000" + str(run) + ".csv"
        path = os.path.join(current_dir, current_file)

        # create a temporary df to start with
        tmp_df = pd.read_csv(path, header=None, delimiter=',')  # your txt or csv file from acqknowledge
        print("Opening file:",current_file )

        # Current columns = EDA, CORR, ECG, Feedback, Stim, ch1-8
        # Let's remove the Corr & Feedback columns
        data = (tmp_df  # make a copy of the df and...
                .drop(index=0)  # remove the first row
                .drop(columns=[1, 3])  # drop columns 1 and 3 (Corr & Feedback)
                .reset_index(drop=True))  # reset row index

        #data.head() # see first few rows
        #print(data)  # take a look at the original data

        # renaming the channels from 0 - 7 instead of 1 - 8 based on Nadu's event code convention
        data.columns = ['EDA', 'ECG', 'Stim', 'ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6',
                        'ch7']

        # Let's label the parent DF (data) and then later, cut out the rows that we want.
        # Create new column - EVENT  and add it to the Data df- fill it with values - flanker start, flanker end, countdown end

        event_conditions = [
            # Distal shock conditions
            ((data['ch0'] == 5) & (data['ch4'] == 5) & (data['ch6'] == 5) &
             (data['ch1'] == 0) & (data['ch2'] == 0) & (data['ch3'] == 0) &
             (data['ch5'] == 0) & (data['ch7'] == 0)),  # distal shock countdown start

            ((data['ch0'] == 5) & (data['ch1'] == 5) & (data['ch3'] == 5) &
             (data['ch4'] == 5) & (data['ch6'] == 5) & (data['ch2'] == 0) &
             (data['ch5'] == 0) & (data['ch7'] == 0)),  # distal shock countdown end *** fixed: channel 0, 1, 3, 4, 6

            ((data['ch2'] == 5) & (data['ch0'] == 0) & (data['ch1'] == 0) &
             (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 0) &
             (data['ch6'] == 0) & (data['ch7'] == 0)),  # distal shock flanker start

            ((data['ch2'] == 5) & (data['ch0'] == 5) & (data['ch1'] == 0) &
             (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 0) &
             (data['ch6'] == 0) & (data['ch7'] == 0)),  # distal shock flanker end

            # Proximal shock conditions
            ((data['ch0'] == 0) & (data['ch1'] == 5) & (data['ch2'] == 0) &
             (data['ch3'] == 0) & (data['ch4'] == 5) & (data['ch5'] == 0) &
             (data['ch6'] == 5) & (data['ch7'] == 0)),  # proximal shock countdown start

            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 5) &
             (data['ch3'] == 5) & (data['ch4'] == 0) & (data['ch5'] == 0) &
             (data['ch6'] == 5) & (data['ch7'] == 0)),  # proximal shock countdown end

            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) &
             (data['ch3'] == 5) & (data['ch4'] == 0) & (data['ch5'] == 0) &
             (data['ch6'] == 0) & (data['ch7'] == 0)),  # proximal shock flanker start

            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) &
             (data['ch3'] == 5) & (data['ch4'] == 0) & (data['ch5'] == 0) &
             (data['ch6'] == 0) & (data['ch7'] == 0)),  # proximal shock flanker end

            # Distal stim conditions
            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 5) &
             (data['ch3'] == 0) & (data['ch4'] == 5) & (data['ch5'] == 0) &
             (data['ch6'] == 5) & (data['ch7'] == 0)),  # distal stim countdown start

            ((data['ch0'] == 0) & (data['ch1'] == 5) & (data['ch2'] == 5) &
             (data['ch3'] == 5) & (data['ch4'] == 5) & (data['ch5'] == 0) &
             (data['ch6'] == 5) & (data['ch7'] == 0)),  # distal stim countdown end *** fixed 1, 2, 3, 4, 6

            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) &
             (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 5) &
             (data['ch6'] == 0) & (data['ch7'] == 0)),  # distal stim flanker start

            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) &
             (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 5) &
             (data['ch6'] == 0) & (data['ch7'] == 0)),  # distal stim flanker end

            # Proximal stim conditions
            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 5) &
             (data['ch3'] == 0) & (data['ch4'] == 5) & (data['ch5'] == 0) &
             (data['ch6'] == 5) & (data['ch7'] == 0)),  # proximal stim countdown start

            ((data['ch2'] == 5) & (data['ch3'] == 5) & (data['ch4'] == 5) &
             (data['ch6'] == 5) & (data['ch0'] == 0) & (data['ch1'] == 0) &
             (data['ch5'] == 0) & (data['ch7'] == 0)),  # proximal shock countdown end *** fixed: channel 2, 3, 4, 6

            ((data['ch0'] == 0) & (data['ch1'] == 0) & (data['ch2'] == 0) &
             (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 0) &
             (data['ch6'] == 5) & (data['ch7'] == 0)),  # proximal stim flanker start

            ((data['ch0'] == 5) & (data['ch1'] == 0) & (data['ch2'] == 0) &
             (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 0) &
             (data['ch6'] == 5) & (data['ch7'] == 0))  # proximal stim flanker end
        ]

        # Define corresponding condition labels in the requested format
        condition_values = [
            'distal shock countdown start',  # 1st condition
            'distal shock countdown end',  # 2nd condition
            'distal shock flanker start',  # 3rd condition
            'distal shock flanker end',  # 4th condition

            'proximal shock countdown start',  # 5th condition
            'proximal shock countdown end',  # 6th condition
            'proximal shock flanker start',  # 7th condition
            'proximal shock flanker end',  # 8th condition

            'distal stim countdown start',  # 9th condition
            'distal stim countdown end',  # 10th condition
            'distal stim flanker start',  # 11th condition
            'distal stim flanker end',  # 12th condition

            'proximal stim countdown start',  # 13th condition
            'proximal stim countdown end',  # 14th condition
            'proximal stim flanker start',  # 15th condition
            'proximal stim flanker end'  # 16th condition
        ]
        print(f"Number of conditions: {len(event_conditions)}")
        print(f"Number of values: {len(condition_values)}")

        # the code below allows us to go through the df and add a col
        # #data['condition'] = np.select(condition_conditions, condition_values, default='none')
        data['EVENT'] = np.select(event_conditions, condition_values, default='none')


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

        # Countdown 1
        # The code below will extract teh first countdown

        index = data['start'].tolist().index('start') + 40
        data_tmp = data.iloc[index:] #from the index to the end of the df
        # reset index
        data_tmp.reset_index(inplace=True, drop=True) #make the row start with 0 again
        # 60 seconds = 60 * 2000 = 120,000 rows - so we take the start and add that many rows to it

        # there is also a 100 ms pause between end of task and end of countdown - 120200 - this finds it - we add those additional rows in
        data_tmp_2 = data_tmp.iloc[0:120400] #get the 1st countdown block
        #row
        # countdown #1 - - - create a df called data_1
        data_1 = data_tmp_2
        # check event codes seen at the end
        # Row 120163: channels 2, 3, 4, 6 - proximal shock- countdown end
        # now the rest of the data starts on row after
        data_rest = data_tmp.iloc[120400:]
        data_rest.reset_index(inplace=True, drop=True) #make the row start with 0 again
        print(data_rest.index)

        # get the index of the end of the start event code from data_rest df
        # if you remove the + 40 you can see the start code
        index = data_rest['start'].tolist().index('start') + 40
        #cut everything before the index
        data_2_tmp = data_rest.iloc[index:] #from the index to the end of the df
        # countdown #2
        data_2_tmp.reset_index(inplace=True, drop=True) #make the row start with 0 again
        print(data_2_tmp.index)
        data_2 = data_2_tmp.iloc[0:120400] #get 2nd countdown
        # check event codes seen at the end- chan 0, 2  - distal shock  - flanker end
        # end row - 120275  - 0, 1, 3, 4, 6 - distal shock end

        # now the second time we cut the data folder and keep the rest - call it data_rest2
        # we start 1 row later
        data_rest2 = data_2_tmp.iloc[120401:]
        data_rest2.reset_index(inplace=True, drop=True)

        # countdown 3
        index = data_rest2['start'].tolist().index('start') +40
        data_tmp_3 = data_rest2.iloc[index:] #from the index to the end of the df
        data_tmp_3.reset_index(inplace=True, drop=True) #make the row start with 0 again
        data_3 = data_tmp_3.iloc[0:120400] #get 3rd countdown
        # check event codes seen at the end -
        data_rest3 = data_tmp_3.iloc[120401:]
        # channel 1, 2, 3, 4, 6  - distal_light_stim countdown end
        data_rest3. reset_index(inplace=True, drop=True)

        # countdown 4
        index = data_rest3['start'].tolist().index('start')   +40
        data_tmp_4 = data_rest3.iloc[index:]  # from the index to the end of the df
        data_tmp_4.reset_index(inplace=True, drop=True)  # make the row start with 0 again
        data_4 = data_tmp_4.iloc[0:120400]  # get 3rd countdown
        # check event codes seen at the end -
        data_rest4 = data_tmp_4.iloc[120401:]
        # check event codes -  0, 1, 2, 3, 4, 6  - proximal_light_stim condition - countdown end

        ######  label the 4 dfs - flanker end - countdown end  ######



        # all we need is eda, event and index
        data_1_save = data_1[['EDA', "Event"]]


        ###### After labelling, take out the important things --- then downsample --- then put in timepoints ########
        # The number "0.01" here dependents on your sampling rate. I have 2000 sampling rate, then I downsampled 20 folds, so now it is 100 sampling rate for the "encoding_downsample". In this case, I use 1/100 = 0.01
        encoding_downsample['timepoint'] = 0.01 * encoding_downsample.index
        # savefile = ID + "_encoding_" + str(run + 1) + ".txt"
        # downsample
        # Select every 20th row
        encoding_downsample = data_1_save[::20]
        encoding_downsample.reset_index(inplace=True, drop=True)
        # add a column for time points.

        # reorder columns
        encoding_downsample = encoding_downsample[['timepoint', 'EDA', 'Event']]
        # remove event code when appeared twice in the same trial - the block of code below does that

        #label full event (including distal, proximal, shock, stim)


        for k in range(len(encoding_downsample)):
            if k < len(encoding_downsample) - 1:
                Code1 = encoding_downsample.loc[k]['Event']
                Code2 = encoding_downsample.loc[k + 1]['Event']
                if int(Code1) > 0 and int(Code2) > 0:
                    indexli.append(k + 1)
        for ind in indexli:
            encoding_downsample.loc[ind, "Event"] = 0
        save = os.path.join(save_dir, savefile)
        encoding_downsample.to_csv(save, header=None, index=None, sep='\t', mode='a')



    # save as txt files here



    # if you want you can append the txt files together into one file


