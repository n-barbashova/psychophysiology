ReadMe:
Also Located here: https://docs.google.com/document/d/1hfkKuHdc5htsAZjkRZWYzMZev2CSRcb4WBH9agrphzE/edit?tab=t.0#heading=h.v4r9sowhak48 


Nadu's Physio Pipeline
This ReadMe has an overview of steps to follow to get EDA and heart rate data from an acq file after using AqKnowledge to collect data. 


EDA Analysis 

### Step 0: Get files from NasDrive 

Make sure acq files are available. Can download them from the Nasdrive - get into the cluster or onto dropbox. It's also ok to use Nasdrive path directly.  

If on campus- connect to tis wifi: psychsecure 
If off campus - connect to the UCSB VPN through Ivanti Secure Access Client. 

You can connect directly to smb://rcl-nas1.psych.ucsb.edu/labshare if you want to mount that share specifically. Note that these are typed differently on Mac vs Windows. On a Windows machine, you would use \\rcl-nas1.psych.ucsb.edu\labshare to connect, with backslashes (\) instead of forward slashes (/).

The user name is PSYCH-ADS\netID (e.g., PSYCH-ADS\jy_wang)

To mount (mac): open finder →  go →  connect to server →  in the popup window (type things below) → click “Connect” 

Before running any of these scripts make sure that the output path of each script is the same as the input path of the next script. 


### Step 1: acqtoCSV_nadu.ipynb

Run this script in a jupyter notebook. 
This script converts the acq files to csv files. 

Input the path of the acq files (Nasdrive path). Create a output directory to store the csv files for each participant and run. 

This script will basically have a row for each timepoint (2000 hz means 2000 rows per second). Each column is a channel, including the physio channels (EDA, ECG, etc and the digital channels, which contain info on the event codes). 

After this step all the physio is in csv format. It can be used for EDA and Heart Rate analysis. 

*** Alternative Step 1: ExportDataToCSV.m 
Alternative script to convert acq file to csv files. I haven’t used this one. 


### Step 2: eda_nadu_pycharm_byRun.py 
Now that the acq data has been converted to a readable format (CSV) we need to label the event codes more clearly and output timing files. 

Before running this script: get the event codes from the PsychoPy file.  Find which event code corresponds with which channels (channels are all binary). 

This script goes through the CSV file, checks all the channels and then finds out which event happened and when, and labels them by adding a label in a newly created Event column. Each event is given a new number that is used as a marker (for instance start of countdown, start of flanker task, etc.) 

At the end, all the data is downsampled and all that is output is the physio data and the timing of the event code. So the output will have a column for EDA, a column for timepoint (in seconds) and a column for the event number.  
 
It will output a timing file (in the form of a .txt file) for each participant and run.  

The 3 columns will not be labelled with a header, but they correspond to this structure: 
timepoint     EDA     EVENT

Events are given a number as a label (in my script ranging 1 to 16). 

To know what condition each event number is tied to, check the condition_values vector 
Example: 1, #'distal shock countdown start',  # 1st condition
Double check that everything is labelled correctly. 
 
### Step 3: Run ledalab: batch_ledalab_command_nadu.m

For this script to work, it needs to be located in the main Ledalab folder, otherwise, Matlab will get confused. Ledalab is not included in MATLAB by default, it needs to be downloaded. 

This script essentially uses one function to loop through a process the data. It will take each txt files from the previous step, process them and then output 3 files - a tif file, .mat and a new text file era.text. 

The tif file is a way to see the EDA and check for non-responders. 
The _era/txt files will be later combined into a DF, and ready to be analyzed. 

There are a few parameters that can be set (such as the time window being analyzed and a few other parameters). 

### Step 4: Physio_analyses_Nadu.rmd 

This is an R script that will:
1) Combine the era.txt files for all runs for all subjects into a CSV (and will export the combined CSV)
2) Convert CDA.ISCR to ISCR_sqPlus1. (ISCR_sqPlus1 is the metric we are interested in examining). 
3) The EDA is ready to be analyzed. All EDA (and HR) analyses follow. 

____________________________________________________________________________  
Heart Rate 

### Step 0: Get files from NasDrive 
If not already done, instructions above.  


### Step 1: acqtoCSV_nadu.ipynb
If not already done, instructions above.  
 
### Step 2: hr_nadu_pycharm.py 
This is very similar to step 2 above, but instead of processing the EDA data it is processing the ECG data and output a timing file for each subject and each run. 

The 3 columns will not be labelled with a header, but they correspond to this structure: 
timepoint    ECG     EVENT

### Step 3: HRV_addEventcodes_Nadu.py
This script adds event codes to the data 


### Step 5: Physio_analyses_Nadu.rmd 
Same as above. Lower blocks process heart rate data. 


