import pandas as pd
import os

Ledadir = "/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz/EDA/EDAprocessed/encoding"
outdir = "/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz/EDA"
IDs = ["006", "007"]
runs = [1, 2, 3, 4, 5, 6]
participant = []
run = []
trialNum2 = []
CDA_ISCR = []
CDA_nSCR = []
CDA_PhasicMax = []
CDA_Tonic = []
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
            CDA_nSCR = CDA_nSCR + data.iloc[:, 1].tolist()
            CDA_PhasicMax = CDA_PhasicMax + data.iloc[:, 6].tolist()
            CDA_Tonic = CDA_Tonic + data.iloc[:, 7].tolist()
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
            Runli = [int(RUN)]*len(data)
            run= run + Runli
            trialNumli_orig = list(range(len(data)))
            trialNumli = [element + 1 for element in trialNumli_orig]
            trialNum2= trialNum2 + trialNumli
            idli = [int(id)]*len(data)
            participant = participant + idli
        except:
            print("Cannot load")
#Make dataframe from the lists and save
df = pd.DataFrame(list(zip(participant,run,trialNum2,CDA_ISCR,CDA_nSCR,CDA_PhasicMax,CDA_Tonic,TTP_AmpSum,TTP_nSCR,EventName)), columns= ["participant", "run", "trialNum2", "CDA.ISCR", "CDA_nSCR", "CDA_PhasicMax", "CDA_Tonic", "TTP.AmpSum", "TTP_nSCR", "EventName"])
Savefile = os.path.join(outdir, "EDAsorted.csv")
print(Savefile)
df.to_csv(Savefile, index=False)