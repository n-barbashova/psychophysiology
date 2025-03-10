# Script for collapsing across digital channels
import pandas as pd
import os
import numpy as np

# check = pd.read_csv('/Users/jingyiwang/Desktop/EB_modified/EB_psychopyz/ivn07_16.txt', delimiter='\t')
save_dir = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/EKG_processed"
rawdata = "/Users/nadezhdabarbashova/Desktop/fmcc_timing/HR/"

IDs = ["49", "50", "51", "52", "54", "55", "56", "57", "58", "61", "62", "63", "65", "67",
            "68", "69", "70", "72", "73", "74"]

#We need to record the start event code conditions for runs so that it can be used for the other analysis
subject = []
runli = []
startcode = []
#Define a function that find the index of not none elements in the list
def find_non_none_indices(lst):
    indices = [i for i, element in enumerate(lst) if element != 'none']
    return indices

def remove_txt_files_in_folder(folder_path):
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path) and file_name.endswith('.txt'):
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            else:
                print(f"Skipping {file_path}. It's either not a file or not a .txt file.")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
#Remove all the txt files from EKG_processed folder
remove_txt_files_in_folder(save_dir)
for ID in IDs:
    for run in range(6):
        subject.append(ID)
        runli.append(run+1)
        current_dir = rawdata + "/" + ID
        current_file = "EB" + ID + "_task1_000" + str(run+2) + ".csv"
        path = os.path.join(current_dir, current_file)

        tmp_df = pd.read_csv(path, header=None, delimiter=',') #your txt or csv file from acqknowledge

        #there is probably a much more sophisticated way to do this, but I check the value of every column for the digital channels
        #check your txt file - I always clean the header and filter out any extra details until I only have the time & channels with the data I want

        data=tmp_df #to make a copy just in case
        #then I rename the channels just slightly because they always seem to be a bit 'off'
        data.columns = ['EDA', 'Corr', 'ECGmV', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8']

        #Use the beginning data before the "start" code: 211
        conditions = [#eventcode=221 => start of block
        (data['ch1'] == 5) & (data['ch2'] == 5) & (data['ch3'] == 0) & (data['ch4'] == 0) & (data['ch5'] == 5) & (data['ch6'] == 0) & (data['ch7'] == 5) & (data['ch8'] == 5)]
        #values
        values = ["start"]
        # then I add a new column to put the start point
        data['start'] = np.select(conditions, values, default="none")

        #divide the dataframe into four sections, two encoding sections, two task sections
        # Find the index of the first occurrence of the value
        #ps: +40 to make sure all the event code for 211 is removed.
        try: 
            index = data['start'].tolist().index('start') + 40

            #Count how many start event code is caught, sometimes some runs only have 1 start event code caught.
            #first get the start_li and downsample
            Start_li = data['start'].tolist()[::20]
            Start_num = find_non_none_indices (Start_li)
            startcode.append(len(Start_num))
            if len(Start_num) == 2:
                #Get the first encoding session
                data_tmp = data.iloc[index:]
                #reset index
                data_tmp.reset_index(inplace=True, drop=True)

                #repeat to make two parts (within a sequence we have two parts)
                index1 = data_tmp['start'].tolist().index('start')
                index2 = index1+20

                data_1 = data_tmp.iloc[:index1]
                # reset index
                data_1.reset_index(inplace=True, drop=True)
                data_2 = data_tmp.iloc[index2:]
                # reset index
                data_2.reset_index(inplace=True, drop=True)
                #then I check the value in every digital channel column and make a 'conditions' list. Then I make a list of the events associated with those conditions
                #Event code conditions: see EventCode_Cheetsheet for details.
                conditions = [
                #So for example, when ch1 is on it is negative image.
                # (data_1['ch1'] == 5) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                #When ch2 is on it is first position, no change = 0
                (data_1['ch1'] == 0) & (data_1['ch2'] == 5) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),

                #When ch3 is on it is color change-within emotion = 1
                (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 5) & (data_1['ch4'] == 0) & (data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                #When ch4 is on it is color change-within neutral = 2
                (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 5) & (data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                #When ch5 is on it is emotional->neutral change = 3
                (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (data_1['ch5'] == 5) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                #When ch6 is on it is neutral->emotional change = 4
                (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (data_1['ch5'] == 0) & (data_1['ch6'] == 5) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                #When ch7 is on it is emotional->neutral change + color = 5
                (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 5) & (data_1['ch8'] == 0),
                #When ch8 is on it is neutral->emotional change + color = 6
                (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 5)
                ]
                #This list is how we decode the values of the event channels, and this corresponds to the conditions list
                #Make sure you have the same # of elements in the conditions and values lists
                # values = ['Neg', '0', '1', '2', '3', '4', '5', '6', 'start']
                values = ['7', '1', '2', '3', '4', '5', '6']

                #then I add a new column to our data frame based on these conditions
                data_1['Event'] = np.select(conditions, values)

                #do the same thing for data_2
                # Event code conditions: see EventCode_Cheetsheet for details.
                conditions = [
                    # So for example, when ch1 is on it is negative image.
                    # (data_2['ch1'] == 5) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (data_2['ch5'] == 0) & (
                    #             data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch2 is on it is first position, no change = 0
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 5) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (data_2['ch5'] == 0) & (
                                data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),

                    # When ch3 is on it is color change-within emotion = 1
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 5) & (data_2['ch4'] == 0) & (data_2['ch5'] == 0) & (
                                data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch4 is on it is color change-within neutral = 2
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 5) & (data_2['ch5'] == 0) & (
                                data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch5 is on it is emotional->neutral change = 3
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (data_2['ch5'] == 5) & (
                                data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch6 is on it is neutral->emotional change = 4
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (data_2['ch5'] == 0) & (
                                data_2['ch6'] == 5) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch7 is on it is emotional->neutral change + color = 5
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (data_2['ch5'] == 0) & (
                                data_2['ch6'] == 0) & (data_2['ch7'] == 5) & (data_2['ch8'] == 0),
                    # When ch8 is on it is neutral->emotional change + color = 6
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (data_2['ch5'] == 0) & (
                                data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 5)
                ]
                # This list is how we decode the values of the event channels, and this corresponds to the conditions list
                # Make sure you have the same # of elements in the conditions and values lists
                # values = ['Neg', '0', '1', '2', '3', '4', '5', '6', 'start']
                values = ['7', '1', '2', '3', '4', '5', '6']

                # then I add a new column to our data frame based on these conditions
                data_2['Event'] = np.select(conditions, values)

                #Break data_1 and data_1 into encoding and task phase
                #First get the code that appeared in the last
                lastcode = data_1['Event'].unique()[4]
                #The lastcode is the last image, we need to add the total time of that trial (6.5s) with sample rate as 2000
                endindex = data_1['Event'][::-1].tolist().index(lastcode)
                endindex = len(data_1) - 1 - endindex
                endindex1 = int(endindex + 6.5*2000)

                #Start of task, basically the end of encoding plus the 45s distraction
                taskstart = int(endindex1 + 45*2000)

                data_1_encoding = data_1[:endindex1]
                data_1_encoding.reset_index(inplace=True, drop=True)
                data_1_task = data_1[taskstart:]
                data_1_task.reset_index(inplace=True, drop=True)

                # Do the same thing for data_2
                # First get the code that appeared in the last
                lastcode = data_2['Event'].unique()[4]
                # The lastcode is the last image, we need to add the total time of that trial (6.5s) with sample rate as 2000
                endindex = data_2['Event'][::-1].tolist().index(lastcode)
                endindex = len(data_2) - 1 - endindex
                endindex2 = int(endindex + 6.5 * 2000)

                # Start of task, basically the end of encoding plus the 45s distraction
                taskstart = int(endindex2 + 45 * 2000)

                data_2_encoding = data_2[:endindex2]
                data_2_encoding.reset_index(inplace=True, drop=True)
                data_2_task = data_2[taskstart:]
                data_2_task.reset_index(inplace=True, drop=True)

                #select useful columns
                data_1_encoding_save = data_1_encoding[['ECGmV',"Event"]]

                data_1_task_save = data_1_task[['ECGmV','Event']]
                data_2_encoding_save = data_2_encoding[['ECGmV', "Event"]]
                data_2_task_save = data_2_task[['ECGmV', 'Event']]

                #Merge the two part of encoding
                encoding = pd.concat([data_1_encoding_save, data_2_encoding_save], ignore_index=True)
                task = pd.concat([data_1_task_save, data_2_task_save], ignore_index=True)

                savefile = ID + "_encodingEKG_" + str(run+1) + ".txt"
                #downsample
                # Select every 20th row
                encoding_downsample = encoding[::20]
                encoding_downsample.reset_index(inplace=True, drop=True)
                # add a column for time points
                encoding_downsample['timepoint'] = 0.01 * encoding_downsample.index
                #reorder columns
                encoding_downsample = encoding_downsample[['timepoint', 'ECGmV','Event']]
                save = os.path.join(save_dir, savefile)
                encoding_downsample.to_csv(save, header=None, index=None, sep='\t', mode='a')

                savefile = ID + "_taskEKG_" + str(run+1) + ".txt"
                save = os.path.join(save_dir, savefile)


                # downsample
                # Select every 20th row
                task_downsample = task[::20]
                task_downsample.reset_index(inplace=True, drop=True)
                # add a column for time points
                task_downsample['timepoint'] = 0.01 * task_downsample.index
                # reorder columns
                task_downsample = task_downsample[['timepoint', 'ECGmV', 'Event']]
                task_downsample.to_csv(save, header=None, index=None, sep='\t', mode='a')
            elif len(Start_num) == 1:
                # Get the first encoding session
                # make two parts (within a sequence we have two parts)
                data_tmp = data
                index1 = data_tmp['start'].tolist().index('start')
                index2 = index1 + 20

                data_1 = data_tmp.iloc[:index1]
                # reset index
                data_1.reset_index(inplace=True, drop=True)
                data_2 = data_tmp.iloc[index2:]
                # reset index
                data_2.reset_index(inplace=True, drop=True)
                # then I check the value in every digital channel column and make a 'conditions' list. Then I make a list of the events associated with those conditions
                # Event code conditions: see EventCode_Cheetsheet for details.
                conditions = [
                    # So for example, when ch1 is on it is negative image.
                    # (data_1['ch1'] == 5) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                    # When ch2 is on it is first position, no change = 0
                    (data_1['ch1'] == 0) & (data_1['ch2'] == 5) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (
                                data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),

                    # When ch3 is on it is color change-within emotion = 1
                    (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 5) & (data_1['ch4'] == 0) & (
                                data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                    # When ch4 is on it is color change-within neutral = 2
                    (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 5) & (
                                data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                    # When ch5 is on it is emotional->neutral change = 3
                    (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (
                                data_1['ch5'] == 5) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                    # When ch6 is on it is neutral->emotional change = 4
                    (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (
                                data_1['ch5'] == 0) & (data_1['ch6'] == 5) & (data_1['ch7'] == 0) & (data_1['ch8'] == 0),
                    # When ch7 is on it is emotional->neutral change + color = 5
                    (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (
                                data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 5) & (data_1['ch8'] == 0),
                    # When ch8 is on it is neutral->emotional change + color = 6
                    (data_1['ch1'] == 0) & (data_1['ch2'] == 0) & (data_1['ch3'] == 0) & (data_1['ch4'] == 0) & (
                                data_1['ch5'] == 0) & (data_1['ch6'] == 0) & (data_1['ch7'] == 0) & (data_1['ch8'] == 5)
                ]
                # This list is how we decode the values of the event channels, and this corresponds to the conditions list
                # Make sure you have the same # of elements in the conditions and values lists
                # values = ['Neg', '0', '1', '2', '3', '4', '5', '6', 'start']
                values = ['7', '1', '2', '3', '4', '5', '6']

                # then I add a new column to our data frame based on these conditions
                data_1['Event'] = np.select(conditions, values)

                # do the same thing for data_2
                # Event code conditions: see EventCode_Cheetsheet for details.
                conditions = [
                    # So for example, when ch1 is on it is negative image.
                    # (data_2['ch1'] == 5) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (data_2['ch5'] == 0) & (
                    #             data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch2 is on it is first position, no change = 0
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 5) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (
                                data_2['ch5'] == 0) & (
                            data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),

                    # When ch3 is on it is color change-within emotion = 1
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 5) & (data_2['ch4'] == 0) & (
                                data_2['ch5'] == 0) & (
                            data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch4 is on it is color change-within neutral = 2
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 5) & (
                                data_2['ch5'] == 0) & (
                            data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch5 is on it is emotional->neutral change = 3
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (
                                data_2['ch5'] == 5) & (
                            data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch6 is on it is neutral->emotional change = 4
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (
                                data_2['ch5'] == 0) & (
                            data_2['ch6'] == 5) & (data_2['ch7'] == 0) & (data_2['ch8'] == 0),
                    # When ch7 is on it is emotional->neutral change + color = 5
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (
                                data_2['ch5'] == 0) & (
                            data_2['ch6'] == 0) & (data_2['ch7'] == 5) & (data_2['ch8'] == 0),
                    # When ch8 is on it is neutral->emotional change + color = 6
                    (data_2['ch1'] == 0) & (data_2['ch2'] == 0) & (data_2['ch3'] == 0) & (data_2['ch4'] == 0) & (
                                data_2['ch5'] == 0) & (
                            data_2['ch6'] == 0) & (data_2['ch7'] == 0) & (data_2['ch8'] == 5)
                ]
                # This list is how we decode the values of the event channels, and this corresponds to the conditions list
                # Make sure you have the same # of elements in the conditions and values lists
                # values = ['Neg', '0', '1', '2', '3', '4', '5', '6', 'start']
                values = ['7', '1', '2', '3', '4', '5', '6']

                # then I add a new column to our data frame based on these conditions
                data_2['Event'] = np.select(conditions, values)

                # Break data_1 and data_1 into encoding and task phase
                # First get the code that appeared in the last
                lastcode = data_1['Event'].unique()[4]
                # The lastcode is the last image, we need to add the total time of that trial (6.5s) with sample rate as 2000
                endindex = data_1['Event'][::-1].tolist().index(lastcode)
                endindex = len(data_1) - 1 - endindex
                endindex1 = int(endindex + 6.5 * 2000)

                # Start of task, basically the end of encoding plus the 45s distraction
                taskstart = int(endindex1 + 45 * 2000)

                data_1_encoding = data_1[:endindex1]
                data_1_encoding.reset_index(inplace=True, drop=True)
                data_1_task = data_1[taskstart:]
                data_1_task.reset_index(inplace=True, drop=True)

                # Do the same thing for data_2
                # First get the code that appeared in the last
                lastcode = data_2['Event'].unique()[4]
                # The lastcode is the last image, we need to add the total time of that trial (6.5s) with sample rate as 2000
                endindex = data_2['Event'][::-1].tolist().index(lastcode)
                endindex = len(data_2) - 1 - endindex
                endindex2 = int(endindex + 6.5 * 2000)

                # Start of task, basically the end of encoding plus the 45s distraction
                taskstart = int(endindex2 + 45 * 2000)

                data_2_encoding = data_2[:endindex2]
                data_2_encoding.reset_index(inplace=True, drop=True)
                data_2_task = data_2[taskstart:]
                data_2_task.reset_index(inplace=True, drop=True)

                # select useful columns
                data_1_encoding_save = data_1_encoding[['ECGmV', "Event"]]

                data_1_task_save = data_1_task[['ECGmV', 'Event']]
                data_2_encoding_save = data_2_encoding[['ECGmV', "Event"]]
                data_2_task_save = data_2_task[['ECGmV', 'Event']]

                # Merge the two part of encoding
                encoding = pd.concat([data_1_encoding_save, data_2_encoding_save], ignore_index=True)
                task = pd.concat([data_1_task_save, data_2_task_save], ignore_index=True)

                savefile = ID + "_encodingEKG_" + str(run + 1) + ".txt"
                # downsample
                # Select every 20th row
                encoding_downsample = encoding[::20]
                encoding_downsample.reset_index(inplace=True, drop=True)
                # add a column for time points
                encoding_downsample['timepoint'] = 0.01 * encoding_downsample.index
                # reorder columns
                encoding_downsample = encoding_downsample[['timepoint', 'ECGmV', 'Event']]
                save = os.path.join(save_dir, savefile)
                encoding_downsample.to_csv(save, header=None, index=None, sep='\t', mode='a')

                savefile = ID + "_taskEKG_" + str(run + 1) + ".txt"
                save = os.path.join(save_dir, savefile)

                # downsample
                # Select every 20th row
                task_downsample = task[::20]
                task_downsample.reset_index(inplace=True, drop=True)
                # add a column for time points
                task_downsample['timepoint'] = 0.01 * task_downsample.index
                # reorder columns
                task_downsample = task_downsample[['timepoint', 'ECGmV', 'Event']]
                task_downsample.to_csv(save, header=None, index=None, sep='\t', mode='a')
        except:
            print("Do not have start code: ID:" + ID + "run: " + str(run + 1))
            startcode.append("NoStartCode")
#Make a dataframe and save the start event code info
#If not run in the EDA process, run here.
# StartCodeSave1 = {
#     'ID': subject,
#     'Run': runli,
#     'StartCodeNum': startcode
# }
#
# StartCodeSave = pd.DataFrame(StartCodeSave1)
# StartCodeSave.to_csv("/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz/StartCodeStatus.csv", index=False)
#         #So now we will have a column filled with the elements in our 'values' lists based on the conditions we gave it in the 'conditions' list
