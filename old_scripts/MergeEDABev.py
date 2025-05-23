import pandas as pd
import os
import ast

Bevdir = "/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz_bev"
EDAdir = "/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz/EDA"
HRVdir = "/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz/HRV"
Corrdir = "/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz/Corrugator"
Outdir = "/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz_bev"
#load encoding spreadsheet
Encodefn = os.path.join(Bevdir, "EB_encode_cleaned.csv")
Encode = pd.read_csv(Encodefn)
#Add run and trialNum2 column
runliwhole = []
runli = [1, 2, 3, 4, 5, 6]
for item in runli:
    for _ in range(32):
        runliwhole.append(item)
runcl = runliwhole*int((len(Encode)/192))
trialli = list(range(1, 33))*6*int((len(Encode)/192))

Encode['run'] = runcl
Encode['trialNum2'] = trialli

#load tempory memory task spreadsheet
Tempfn = os.path.join(Bevdir, "EB_temporal_cleaned.csv")
Temp = pd.read_csv(Tempfn)

#Load EDA spreadsheet
EDAfn = os.path.join(EDAdir, "EDAsorted.csv")
EDA = pd.read_csv(EDAfn)

#Load HRV spreadsheet
HRVfn = os.path.join(HRVdir, "HRVtrialwiseall.csv")
HRV = pd.read_csv(HRVfn)

#Load Corrugator spreadsheet
Corrfn = os.path.join(Corrdir, "EMGtrialwiseall.csv")
Corr = pd.read_csv(Corrfn)

#Merge Encoding and EDA and HRV
EncodeEDA = pd.merge(EDA, Encode, on=['participant', 'run', 'trialNum2'], how='right')
EncodeEDAHRV = pd.merge(HRV, EncodeEDA, on=['participant', 'run', 'trialNum2'], how='right')
EncodeEDAHRV = pd.merge(Corr, EncodeEDAHRV, on=['participant', 'run', 'trialNum2'], how='right')
#Add the clean IAP image name column
def remove_prefix_postfix(cell_value):
    prefix1 = 'StimusNeu/'
    prefix2 = 'StimusEmo/'
    postfix1 = '.jpg'
    postfix2 = '.JPG'
    if cell_value.startswith(prefix1):
        cell_value = cell_value[len(prefix1):]
    if cell_value.startswith(prefix2):
        cell_value = cell_value[len(prefix2):]
    if cell_value.endswith(postfix1):
        cell_value = cell_value[:-len(postfix1)]
    if cell_value.endswith(postfix2):
        cell_value = cell_value[:-len(postfix2)]
    return cell_value
# Add a new column with the prefix and postfix removed
EncodeEDAHRV['IAPS'] = EncodeEDAHRV['event_images'].apply(remove_prefix_postfix)
EncodeEDAHRV['IAPS'] = EncodeEDAHRV['IAPS'].astype(float)

#Add the normative rating and image file name
#load the IAPS spreadsheet
IAPS = pd.read_excel("/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_modified_analyses/EB3_analyses/Master_IAPS_August_2009.xls",  usecols=['IAPS', 'valmn', 'aromn'])
#Merge to add normative arousal and valence rating
EncodeEDAHRV = pd.merge(EncodeEDAHRV,IAPS, on="IAPS", how='left', sort=False)

savefn = os.path.join(Outdir, "EB_encode_cleaned_EDAHRVEMG.csv")
EncodeEDAHRV.to_csv(savefn, index=False)

#Merge Temporal with EDA and HRV
FirstImg_CDAISCR = []
SecondImg_CDAISCR = []
EDAdiff_CDAISCR = []

FirstImg_CDAnSCR = []
SecondImg_CDAnSCR = []
EDAdiff_CDAnSCR = []

FirstImg_CDAPhasicMax = []
SecondImg_CDAPhasicMax = []
EDAdiff_CDAPhasicMax = []

FirstImg_CDATonic = []
SecondImg_CDATonic = []
EDAdiff_CDATonic = []

FirstImg_TTPAmpSum = []
SecondImg_TTPAmpSum = []
EDAdiff_TTPAmpSum = []

FirstImg_TTPnSCR = []
SecondImg_TTPnSCR = []
EDAdiff_TTPnSCR = []

#Corr_parameters
FirstImg_CorrPower_z = []
SecondImg_CorrPower_z = []
CorrPower_z_diff = []

#HRV parameters
FirstImg_HROnset = []
SecondImg_HROnset = []

FirstImg_HRtrialmax = []
SecondImg_HRtrialmax = []

FirstImg_HRtrialave = []
SecondImg_HRtrialave = []

FirstImg_HRtrialmin = []
SecondImg_HRtrialmin = []

FirstImg_HRtrialbeta = []
SecondImg_HRtrialbeta = []

FirstImg_HRtrialIntercept = []
SecondImg_HRtrialIntercept = []

FirstImg_powLFOnset = []
SecondImg_powLFOnset = []

FirstImg_powHFOnset = []
SecondImg_powHFOnset = []

FirstImg_powLFvsHFOnset = []
SecondImg_powLFvsHFOnset = []

FirstImg_powLFtrialave = []
SecondImg_powLFtrialave = []

FirstImg_powHFtrialave = []
SecondImg_powHFtrialave = []

FirstImg_powLFvsHFtrialave = []
SecondImg_powLFvsHFtrialave = []

FirstImg_powLFtrialmax = []
SecondImg_powLFtrialmax = []

FirstImg_powHFtrialmax = []
SecondImg_powHFtrialmax = []

FirstImg_powLFvsHFtrialmax = []
SecondImg_powLFvsHFtrialmax = []

FirstImg_powLFtrialmin = []
SecondImg_powLFtrialmin = []

FirstImg_powHFtrialmin = []
SecondImg_powHFtrialmin = []

FirstImg_powLFvsHFtrialmin = []
SecondImg_powLFvsHFtrialmin = []


bdcond = []
run = []
trialNumFirst = []
trialNumSecond = []

for ind, row in Temp.iterrows():
    tmppair = row['current_pair_tested']
    tmp = ast.literal_eval(tmppair)
    trial1 = EncodeEDAHRV.index[(EncodeEDAHRV['event_images']==tmp[0]) & (EncodeEDAHRV['participant']==row['participant'])].tolist()[0]
    trial2 = EncodeEDAHRV.index[(EncodeEDAHRV['event_images']==tmp[1]) & (EncodeEDAHRV['participant']==row['participant'])].tolist()[0]
    if trial1 > trial2:
        FirstImg_CorrPower_z.append(EncodeEDAHRV.iloc[trial2]['CorrPower_z'])
        SecondImg_CorrPower_z.append(EncodeEDAHRV.iloc[trial1]['CorrPower_z'])
        CorrPower_z_diff.append(EncodeEDAHRV.iloc[trial2]['CorrPower_z'] - EncodeEDAHRV.iloc[trial1]['CorrPower_z'])

        FirstImg_CDAISCR.append(EncodeEDAHRV.iloc[trial2]['CDA.ISCR'])
        SecondImg_CDAISCR.append(EncodeEDAHRV.iloc[trial1]['CDA.ISCR'])
        EDAdiff_CDAISCR.append(EncodeEDAHRV.iloc[trial2]['CDA.ISCR'] - EncodeEDAHRV.iloc[trial1]['CDA.ISCR'])

        FirstImg_CDAnSCR.append(EncodeEDAHRV.iloc[trial2]['CDA_nSCR'])
        SecondImg_CDAnSCR.append(EncodeEDAHRV.iloc[trial1]['CDA_nSCR'])
        EDAdiff_CDAnSCR.append(EncodeEDAHRV.iloc[trial2]['CDA_nSCR'] - EncodeEDAHRV.iloc[trial1]['CDA_nSCR'])

        FirstImg_CDAPhasicMax.append(EncodeEDAHRV.iloc[trial2]['CDA_PhasicMax'])
        SecondImg_CDAPhasicMax.append(EncodeEDAHRV.iloc[trial1]['CDA_PhasicMax'])
        EDAdiff_CDAPhasicMax.append(EncodeEDAHRV.iloc[trial2]['CDA_PhasicMax'] - EncodeEDAHRV.iloc[trial1]['CDA_PhasicMax'])

        FirstImg_CDATonic.append(EncodeEDAHRV.iloc[trial2]['CDA_Tonic'])
        SecondImg_CDATonic.append(EncodeEDAHRV.iloc[trial1]['CDA_Tonic'])
        EDAdiff_CDATonic.append(EncodeEDAHRV.iloc[trial2]['CDA_Tonic'] - EncodeEDAHRV.iloc[trial1]['CDA_Tonic'])

        FirstImg_TTPAmpSum.append(EncodeEDAHRV.iloc[trial2]['TTP.AmpSum'])
        SecondImg_TTPAmpSum.append(EncodeEDAHRV.iloc[trial1]['TTP.AmpSum'])
        EDAdiff_TTPAmpSum.append(EncodeEDAHRV.iloc[trial2]['TTP.AmpSum'] - EncodeEDAHRV.iloc[trial1]['TTP.AmpSum'])

        FirstImg_TTPnSCR.append(EncodeEDAHRV.iloc[trial2]['TTP_nSCR'])
        SecondImg_TTPnSCR.append(EncodeEDAHRV.iloc[trial1]['TTP_nSCR'])
        EDAdiff_TTPnSCR.append(EncodeEDAHRV.iloc[trial2]['TTP_nSCR'] - EncodeEDAHRV.iloc[trial1]['TTP_nSCR'])

        #For the HRV parameters
        FirstImg_HROnset.append(EncodeEDAHRV.iloc[trial2]['HROnset'])
        SecondImg_HROnset.append(EncodeEDAHRV.iloc[trial1]['HROnset'])

        FirstImg_HRtrialmax.append(EncodeEDAHRV.iloc[trial2]['HRtrialmax'])
        SecondImg_HRtrialmax.append(EncodeEDAHRV.iloc[trial1]['HRtrialmax'])

        FirstImg_HRtrialave.append(EncodeEDAHRV.iloc[trial2]['HRtrialave'])
        SecondImg_HRtrialave.append(EncodeEDAHRV.iloc[trial1]['HRtrialave'])

        FirstImg_HRtrialmin.append(EncodeEDAHRV.iloc[trial2]['HRtrialmin'])
        SecondImg_HRtrialmin.append(EncodeEDAHRV.iloc[trial1]['HRtrialmin'])

        FirstImg_HRtrialbeta.append(EncodeEDAHRV.iloc[trial2]['HRtrialbeta'])
        SecondImg_HRtrialbeta.append(EncodeEDAHRV.iloc[trial1]['HRtrialbeta'])

        FirstImg_HRtrialIntercept.append(EncodeEDAHRV.iloc[trial2]['HRtrialIntercept'])
        SecondImg_HRtrialIntercept.append(EncodeEDAHRV.iloc[trial1]['HRtrialIntercept'])

        FirstImg_powLFOnset.append(EncodeEDAHRV.iloc[trial2]['powLFOnset'])
        SecondImg_powLFOnset.append(EncodeEDAHRV.iloc[trial1]['powLFOnset'])

        FirstImg_powHFOnset.append(EncodeEDAHRV.iloc[trial2]['powHFOnset'])
        SecondImg_powHFOnset.append(EncodeEDAHRV.iloc[trial1]['powHFOnset'])

        FirstImg_powLFvsHFOnset.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFOnset'])
        SecondImg_powLFvsHFOnset.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFOnset'])

        FirstImg_powLFtrialave.append(EncodeEDAHRV.iloc[trial2]['powLFtrialave'])
        SecondImg_powLFtrialave.append(EncodeEDAHRV.iloc[trial1]['powLFtrialave'])

        FirstImg_powHFtrialave.append(EncodeEDAHRV.iloc[trial2]['powHFtrialave'])
        SecondImg_powHFtrialave.append(EncodeEDAHRV.iloc[trial1]['powHFtrialave'])

        FirstImg_powLFvsHFtrialave.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFtrialave'])
        SecondImg_powLFvsHFtrialave.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFtrialave'])

        FirstImg_powLFtrialmax.append(EncodeEDAHRV.iloc[trial2]['powLFtrialmax'])
        SecondImg_powLFtrialmax.append(EncodeEDAHRV.iloc[trial1]['powLFtrialmax'])

        FirstImg_powHFtrialmax.append(EncodeEDAHRV.iloc[trial2]['powHFtrialmax'])
        SecondImg_powHFtrialmax.append(EncodeEDAHRV.iloc[trial1]['powHFtrialmax'])

        FirstImg_powLFvsHFtrialmax.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFtrialmax'])
        SecondImg_powLFvsHFtrialmax.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFtrialmax'])

        FirstImg_powLFtrialmin.append(EncodeEDAHRV.iloc[trial2]['powLFtrialmin'])
        SecondImg_powLFtrialmin.append(EncodeEDAHRV.iloc[trial1]['powLFtrialmin'])

        FirstImg_powHFtrialmin.append(EncodeEDAHRV.iloc[trial2]['powHFtrialmin'])
        SecondImg_powHFtrialmin.append(EncodeEDAHRV.iloc[trial1]['powHFtrialmin'])

        FirstImg_powLFvsHFtrialmin.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFtrialmin'])
        SecondImg_powLFvsHFtrialmin.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFtrialmin'])

        bdcond.append(EncodeEDAHRV.iloc[trial1]['bdcond'])
        run.append(EncodeEDAHRV.iloc[trial1]['run'])
        trialNumFirst.append(EncodeEDAHRV.iloc[trial2]['trialNum2'])
        trialNumSecond.append(EncodeEDAHRV.iloc[trial1]['trialNum2'])
    else:
        FirstImg_CorrPower_z.append(EncodeEDAHRV.iloc[trial1]['CorrPower_z'])
        SecondImg_CorrPower_z.append(EncodeEDAHRV.iloc[trial2]['CorrPower_z'])
        CorrPower_z_diff.append(EncodeEDAHRV.iloc[trial1]['CorrPower_z'] - EncodeEDAHRV.iloc[trial2]['CorrPower_z'])

        FirstImg_CDAISCR.append(EncodeEDAHRV.iloc[trial1]['CDA.ISCR'])
        SecondImg_CDAISCR.append(EncodeEDAHRV.iloc[trial2]['CDA.ISCR'])
        EDAdiff_CDAISCR.append(EncodeEDAHRV.iloc[trial1]['CDA.ISCR'] - EncodeEDAHRV.iloc[trial2]['CDA.ISCR'])

        FirstImg_CDAnSCR.append(EncodeEDAHRV.iloc[trial1]['CDA_nSCR'])
        SecondImg_CDAnSCR.append(EncodeEDAHRV.iloc[trial2]['CDA_nSCR'])
        EDAdiff_CDAnSCR.append(EncodeEDAHRV.iloc[trial1]['CDA_nSCR'] - EncodeEDAHRV.iloc[trial2]['CDA_nSCR'])

        FirstImg_CDAPhasicMax.append(EncodeEDAHRV.iloc[trial1]['CDA_PhasicMax'])
        SecondImg_CDAPhasicMax.append(EncodeEDAHRV.iloc[trial2]['CDA_PhasicMax'])
        EDAdiff_CDAPhasicMax.append(EncodeEDAHRV.iloc[trial1]['CDA_PhasicMax'] - EncodeEDAHRV.iloc[trial2]['CDA_PhasicMax'])

        FirstImg_CDATonic.append(EncodeEDAHRV.iloc[trial1]['CDA_Tonic'])
        SecondImg_CDATonic.append(EncodeEDAHRV.iloc[trial2]['CDA_Tonic'])
        EDAdiff_CDATonic.append(EncodeEDAHRV.iloc[trial1]['CDA_Tonic'] - EncodeEDAHRV.iloc[trial2]['CDA_Tonic'])

        FirstImg_TTPAmpSum.append(EncodeEDAHRV.iloc[trial1]['TTP.AmpSum'])
        SecondImg_TTPAmpSum.append(EncodeEDAHRV.iloc[trial2]['TTP.AmpSum'])
        EDAdiff_TTPAmpSum.append(EncodeEDAHRV.iloc[trial1]['TTP.AmpSum'] - EncodeEDAHRV.iloc[trial2]['TTP.AmpSum'])

        FirstImg_TTPnSCR.append(EncodeEDAHRV.iloc[trial1]['TTP_nSCR'])
        SecondImg_TTPnSCR.append(EncodeEDAHRV.iloc[trial2]['TTP_nSCR'])
        EDAdiff_TTPnSCR.append(EncodeEDAHRV.iloc[trial1]['TTP_nSCR'] - EncodeEDAHRV.iloc[trial2]['TTP_nSCR'])

        # For the HRV parameters
        FirstImg_HROnset.append(EncodeEDAHRV.iloc[trial1]['HROnset'])
        SecondImg_HROnset.append(EncodeEDAHRV.iloc[trial2]['HROnset'])

        FirstImg_HRtrialmax.append(EncodeEDAHRV.iloc[trial1]['HRtrialmax'])
        SecondImg_HRtrialmax.append(EncodeEDAHRV.iloc[trial2]['HRtrialmax'])

        FirstImg_HRtrialave.append(EncodeEDAHRV.iloc[trial1]['HRtrialave'])
        SecondImg_HRtrialave.append(EncodeEDAHRV.iloc[trial2]['HRtrialave'])

        FirstImg_HRtrialmin.append(EncodeEDAHRV.iloc[trial1]['HRtrialmin'])
        SecondImg_HRtrialmin.append(EncodeEDAHRV.iloc[trial2]['HRtrialmin'])

        FirstImg_HRtrialbeta.append(EncodeEDAHRV.iloc[trial1]['HRtrialbeta'])
        SecondImg_HRtrialbeta.append(EncodeEDAHRV.iloc[trial2]['HRtrialbeta'])

        FirstImg_HRtrialIntercept.append(EncodeEDAHRV.iloc[trial1]['HRtrialIntercept'])
        SecondImg_HRtrialIntercept.append(EncodeEDAHRV.iloc[trial2]['HRtrialIntercept'])

        FirstImg_powLFOnset.append(EncodeEDAHRV.iloc[trial1]['powLFOnset'])
        SecondImg_powLFOnset.append(EncodeEDAHRV.iloc[trial2]['powLFOnset'])

        FirstImg_powHFOnset.append(EncodeEDAHRV.iloc[trial1]['powHFOnset'])
        SecondImg_powHFOnset.append(EncodeEDAHRV.iloc[trial2]['powHFOnset'])

        FirstImg_powLFvsHFOnset.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFOnset'])
        SecondImg_powLFvsHFOnset.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFOnset'])

        FirstImg_powLFtrialave.append(EncodeEDAHRV.iloc[trial1]['powLFtrialave'])
        SecondImg_powLFtrialave.append(EncodeEDAHRV.iloc[trial2]['powLFtrialave'])

        FirstImg_powHFtrialave.append(EncodeEDAHRV.iloc[trial1]['powHFtrialave'])
        SecondImg_powHFtrialave.append(EncodeEDAHRV.iloc[trial2]['powHFtrialave'])

        FirstImg_powLFvsHFtrialave.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFtrialave'])
        SecondImg_powLFvsHFtrialave.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFtrialave'])

        FirstImg_powLFtrialmax.append(EncodeEDAHRV.iloc[trial1]['powLFtrialmax'])
        SecondImg_powLFtrialmax.append(EncodeEDAHRV.iloc[trial2]['powLFtrialmax'])

        FirstImg_powHFtrialmax.append(EncodeEDAHRV.iloc[trial1]['powHFtrialmax'])
        SecondImg_powHFtrialmax.append(EncodeEDAHRV.iloc[trial2]['powHFtrialmax'])

        FirstImg_powLFvsHFtrialmax.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFtrialmax'])
        SecondImg_powLFvsHFtrialmax.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFtrialmax'])

        FirstImg_powLFtrialmin.append(EncodeEDAHRV.iloc[trial1]['powLFtrialmin'])
        SecondImg_powLFtrialmin.append(EncodeEDAHRV.iloc[trial2]['powLFtrialmin'])

        FirstImg_powHFtrialmin.append(EncodeEDAHRV.iloc[trial1]['powHFtrialmin'])
        SecondImg_powHFtrialmin.append(EncodeEDAHRV.iloc[trial2]['powHFtrialmin'])

        FirstImg_powLFvsHFtrialmin.append(EncodeEDAHRV.iloc[trial1]['powLFvsHFtrialmin'])
        SecondImg_powLFvsHFtrialmin.append(EncodeEDAHRV.iloc[trial2]['powLFvsHFtrialmin'])

        bdcond.append(EncodeEDAHRV.iloc[trial2]['bdcond'])
        run.append(EncodeEDAHRV.iloc[trial2]['run'])
        trialNumFirst.append(EncodeEDAHRV.iloc[trial1]['trialNum2'])
        trialNumSecond.append(EncodeEDAHRV.iloc[trial2]['trialNum2'])

Temp['FirstImg_CorrPower_z'] = FirstImg_CorrPower_z
Temp['SecondImg_CorrPower_z'] = SecondImg_CorrPower_z
Temp['CorrPower_z_diff'] = CorrPower_z_diff

Temp['FirstImg_CDAISCR'] = FirstImg_CDAISCR
Temp['SecondImg_CDAISCR'] = SecondImg_CDAISCR
Temp['EDAdiff_CDAISCR'] = EDAdiff_CDAISCR

Temp['FirstImg_CDAnSCR'] = FirstImg_CDAnSCR
Temp['SecondImg_CDAnSCR'] = SecondImg_CDAnSCR
Temp['EDAdiff_CDAnSCR'] = EDAdiff_CDAnSCR

Temp['FirstImg_CDAPhasicMax'] = FirstImg_CDAPhasicMax
Temp['SecondImg_CDAPhasicMax'] = SecondImg_CDAPhasicMax
Temp['EDAdiff_CDAPhasicMax'] = EDAdiff_CDAPhasicMax

Temp['FirstImg_CDATonic'] = FirstImg_CDATonic
Temp['SecondImg_CDATonic'] = SecondImg_CDATonic
Temp['EDAdiff_CDATonic'] = EDAdiff_CDATonic

Temp['FirstImg_TTPAmpSum'] = FirstImg_TTPAmpSum
Temp['SecondImg_TTPAmpSum'] = SecondImg_TTPAmpSum
Temp['EDAdiff_TTPAmpSum'] = EDAdiff_TTPAmpSum

Temp['FirstImg_TTPnSCR'] = FirstImg_TTPnSCR
Temp['SecondImg_TTPnSCR'] = SecondImg_TTPnSCR
Temp['EDAdiff_TTPnSCR'] = EDAdiff_TTPnSCR

Temp['FirstImg_HROnset'] = FirstImg_HROnset
Temp['SecondImg_HROnset'] = SecondImg_HROnset

Temp['FirstImg_HRtrialmax'] = FirstImg_HRtrialmax
Temp['SecondImg_HRtrialmax'] = SecondImg_HRtrialmax

Temp['FirstImg_HRtrialave'] = FirstImg_HRtrialave
Temp['SecondImg_HRtrialave'] = SecondImg_HRtrialave

Temp['FirstImg_HRtrialmin'] = FirstImg_HRtrialmin
Temp['SecondImg_HRtrialmin'] = SecondImg_HRtrialmin

Temp['FirstImg_HRtrialbeta'] = FirstImg_HRtrialbeta
Temp['SecondImg_HRtrialbeta']= SecondImg_HRtrialbeta

Temp['FirstImg_HRtrialIntercept'] = FirstImg_HRtrialIntercept
Temp['SecondImg_HRtrialIntercept'] = SecondImg_HRtrialIntercept

Temp['FirstImg_powLFOnset'] = FirstImg_powLFOnset
Temp['SecondImg_powLFOnset'] = SecondImg_powLFOnset

Temp['FirstImg_powHFOnset'] = FirstImg_powHFOnset
Temp['SecondImg_powHFOnset'] = SecondImg_powHFOnset

Temp['FirstImg_powLFvsHFOnset'] = FirstImg_powLFvsHFOnset
Temp['SecondImg_powLFvsHFOnset'] = SecondImg_powLFvsHFOnset

Temp['FirstImg_powLFtrialave'] = FirstImg_powLFtrialave
Temp['SecondImg_powLFtrialave'] = SecondImg_powLFtrialave

Temp['FirstImg_powHFtrialave'] = FirstImg_powHFtrialave
Temp['SecondImg_powHFtrialave'] = SecondImg_powHFtrialave

Temp['FirstImg_powLFvsHFtrialave'] = FirstImg_powLFvsHFtrialave
Temp['SecondImg_powLFvsHFtrialave'] = SecondImg_powLFvsHFtrialave

Temp['FirstImg_powLFtrialmax'] = FirstImg_powLFtrialmax
Temp['SecondImg_powLFtrialmax'] = SecondImg_powLFtrialmax

Temp['FirstImg_powHFtrialmax'] = FirstImg_powHFtrialmax
Temp['SecondImg_powHFtrialmax'] = SecondImg_powHFtrialmax

Temp['FirstImg_powLFvsHFtrialmax'] = FirstImg_powLFvsHFtrialmax
Temp['SecondImg_powLFvsHFtrialmax'] = SecondImg_powLFvsHFtrialmax

Temp['FirstImg_powLFtrialmin'] = FirstImg_powLFtrialmin
Temp['SecondImg_powLFtrialmin'] = SecondImg_powLFtrialmin

Temp['FirstImg_powHFtrialmin'] = FirstImg_powHFtrialmin
Temp['SecondImg_powHFtrialmin'] = SecondImg_powHFtrialmin

Temp['FirstImg_powLFvsHFtrialmin'] = FirstImg_powLFvsHFtrialmin
Temp['SecondImg_powLFvsHFtrialmin'] = SecondImg_powLFvsHFtrialmin


Temp['bdcond_EDA'] = bdcond
Temp['run'] = run
Temp['trialNumFirst'] = trialNumFirst
Temp['trialNumSecond'] = trialNumSecond


print("done")
#Save
savefn = os.path.join(Outdir, "EB_temporal_cleaned_EDAHRVCorr.csv")
Temp.to_csv(savefn, index=False)

