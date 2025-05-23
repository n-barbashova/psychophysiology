%ledalab('/Users/greischar/Eime_pilot/em030/work/','open','text','smooth',{
%'adapt',0},'analyze','CDA', 'optimize',3, 'export_era', [1 4 .02 2],'overview',1) 


addpath(genpath('/Users/nadezhdabarbashova/Library/CloudStorage/Dropbox/LEAP_Neuro_Lab/resources/EDA/ledalab-349'))

%'/Users/jingyiwang/Desktop/AA_fMRIAnalyses/EDAAnalysis/EDAprocessed/' this folder contain all the matlab processed data. 
%Ledalab('/Users/jingyiwang/Desktop/EB_modified/EB_psychopyz/EDAprocessed/','open','text','filter',[3 1], 'downsample',500,'smooth', {'adapt',28},'analyze','CDA', 'optimize',3, 'export_era', [1 5 .02 2],'overview',1) 

% downsample - downsample by a factor of 10 (we already downnsampled a lot
% in the EDA script 
% smooth - run a smoothing function on the curve  - reduce noise 
% CDA - composition analysis 

% make sure ALL the txt files are in one folder 
% [1 4 .01 2] - time window we analyze - threshold 

% more info on all the parameters here: 
% https://lapatewiki.psych.ucsb.edu/index.php/Skin_Conductance_(EDA)  

Ledalab('/Users/nadezhdabarbashova/Desktop/fmcc_timing_30s/','open','text', 'downsample',10,'smooth', {'adapt',28},'analyze','CDA', 'optimize',3, 'export_era', [1 30 .01 2],'overview',1) 


