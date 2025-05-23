import pandas as pd
import os

Ledadir = "/zwork/jingyi/EB/EBpsychopyz_NegNeu/EDA/EDAprocessed/encoding"
outdir = "/zwork/jingyi/EB/EBpsychopyz_NegNeu/EDA"
IDs = ["006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "035", "036", "037", "038", "040", "041", "042", "043", "044", "045", "046", "047", "048", "049", "050", "051", "052", "053", "054", "055", "056", "057", "059", "060", "062", "063", "064", "065", "066", "067", "068", "069"]
runs = [1, 2, 3, 4, 5, 6]
participant = []
run = []
trialNum2 = []
CDA_ISCR = []
TTP_AmpSum = []
TTP_nSCR = []
EventName = []
for id in IDs:
    for RUN in runs:
        try:
            currentFile = id + "_encoding_"+ str(RUN) + "_era.txt"
            LedaFile = os.path.join(Ledadir, currentFile)
            data = pd.read_csv(LedaFile, sep='\t', header=None, skiprows=1)
            CDA_ISCR = CDA_ISCR + data.iloc[:, 5].tolist()
            TTP_AmpSum = TTP_AmpSum + data.iloc[:,10].tolist()
            TTP_nSCR = TTP_nSCR + data.iloc[:,8].tolist()
            EventName = EventName + data.iloc[:,14].tolist()
            # if RUN==1: #todo change to 0
            #     CDA_ISCR = data.iloc[:, 5]
            #     TTP_AmpSum = data.iloc[:, 10]
            #     TTP_nSCR = data.iloc[:, 8]
            #     EventName = data.iloc[:, 14]
            # else:
            #     CDA_ISCR = CDA_ISCR + data.iloc[:,5]
            #     TTP_AmpSum = TTP_AmpSum + data.iloc[:,10]
            #     TTP_nSCR = TTP_nSCR + data.iloc[:,8]
            #     EventName = EventName + data.iloc[:,14]
            Runli = [int(RUN)]*len(EventName)
            run= run + Runli
            trialNumli_orig = list(range(len(EventName)))
            trialNumli = [element + 1 for element in trialNumli_orig]
            trialNum2= trialNum2 + trialNumli
            idli = [int(id)]*len(EventName)
            participant = participant + idli
        except:
            print("Cannot open: ID: " + id + " run: " + str(RUN))


#Make dataframe from the lists and save
df = pd.DataFrame(list(zip(participant,run,trialNum2,CDA_ISCR,TTP_AmpSum,TTP_nSCR,EventName)), columns= ["participant", "run", "trialNum2", "CDA.ISCR", "TTP.AmpSum", "TTP_nSCR", "EventName"])
Savefile = os.path.join(outdir, "EDAsorted.csv")
df.to_csv(Savefile, index=False)