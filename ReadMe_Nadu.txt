ReadMe:

Nadu's Pipeline: 
EDA Analysis 


Step 0: Get files from NasDrive 
Make sure acq files are available. Can download them from the Nasdrive - get into the cluster or onto dropbox. It's also ok to use Nasdrive path. 

You can connect directly to smb://rcl-nas1.psych.ucsb.edu/labshare if you want to mount that share specifically. Note that these are typed differently on Mac vs Windows. On a Windows machine, you would use \\rcl-nas1.psych.ucsb.edu\labshare to connect, with backslashes (\) instead of forward slashes (/).

The user name is PSYCH-ADS\netID (e.g., PSYCH-ADS\jy_wang)

To mount (mac): open finder →  go →  connect to server →  in the popup window (type things below) → click “Connect” 



Step 1: acqtoCSV_nadu.ipynb

Run this in jupyter notebook. 
This script converts the acq files to csv files. 

Input the path of the acq files (Nasdrive path). Create a output directory to store the csv files for each participant and run. 

This script will basically have a row for each timepoint (2000 hz means 2000 rows per second). Each column is a channel, including the physio channels (EDA, ECG, etc and the digital channels, which contain info on the the event codes). 

* Step 1: ExportDataToCSV.m 
Alternative script to convert acq file to csv files. 


Step 2: EventCodes.py: put event code in

eda_nadu_pycharm.py 


Before running this script: get the event codes from the PsychoPy file. 
Find which event code corresponds with which channels (channels are all binary). 
This script goes through the CSV file, checks all the channels and then finds out which event happened and when. Each event is given a new number that is used as a marker (for instance start of countdown, start of flanker task, etc.) 

At the end it is downsampled and all that is output is the physio data and the timing of the event code. So the output will have a column for EDA, a column for timepoint (in seconds) and a column for the event number.  
 
 
Step 3: Run leda lab: 
batch_ledalab_command.m


Step 4: SortLedalabOutput.py


Step 5: MergeEDABev.py (this can merge EDA metrics to EB_encode_cleaned.csv and EB_temporal_cleaned.csv) 




Heart Rate 

hr_nadu_pycharm.py 

HRV_addEventcodes_Nadu.py


# analyze EDA and HR: 
Physio_analyses_Nadu.rmd 

