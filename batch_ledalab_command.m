%ledalab('/Users/greischar/Eime_pilot/em030/work/','open','text','smooth',{
%'adapt',0},'analyze','CDA', 'optimize',3, 'export_era', [1 4 .02 2],'overview',1) 


addpath(genpath('/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/ASAP_training/ledalab-349/'))

%'/Users/jingyiwang/Desktop/AA_fMRIAnalyses/EDAAnalysis/EDAprocessed/' this folder contain all the matlab processed data. 
%Ledalab('/Users/jingyiwang/Desktop/EB_modified/EB_psychopyz/EDAprocessed/','open','text','filter',[3 1], 'downsample',500,'smooth', {'adapt',28},'analyze','CDA', 'optimize',3, 'export_era', [1 5 .02 2],'overview',1) 

Ledalab('/Users/jingyiwang/Dropbox/LEAP_Neuro_Lab/researchProjects/jingyi_documents/EmotionBoundaryInteraction/EB_psychopyz_analyses/EB_psychopyz/EDA/EDAprocessed/','open','text', 'downsample',10,'smooth', {'adapt',28},'analyze','CDA', 'optimize',3, 'export_era', [1 4 .01 2],'overview',1) 







