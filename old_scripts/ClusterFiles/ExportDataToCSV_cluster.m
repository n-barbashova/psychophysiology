clear;
biopacmat_dir = '/zwork/jingyi/EB/EBpsychopyz_NegNeu/rawdata/EB_Psy_data/';
out_dir = '/zwork/jingyi/EB/EBpsychopyz_NegNeu/rawdata_sorted/';

% %for participants 6-9
% %only include normal participant's ID
% %IDlist_1 = [6, 7, 9];
% IDlist_1 = [6];
% runNum = 7; % 6 runs in total
% %pids = 9; %last PID in list
% for ipid = 1:length(IDlist_1)
%     for irun=2:runNum
%         %Task1 (EB)
%         %Load each mat file
%         fileload = [biopacmat_dir '00' num2str(IDlist_1(ipid)) '/EB00' num2str(IDlist_1(ipid)) '_task1_000' num2str(irun) '.mat'];
%         load(fileload);
%         %Create output directory
%         outputdir = [out_dir '00' num2str(IDlist_1(ipid))];
%         % Check if the folder exists
%         if ~exist(outputdir, 'dir')
%             % If the folder doesn't exist, create it
%             mkdir(outputdir);
%         end
%         %write each mat file into csv
%         output_name = [out_dir '00' num2str(IDlist_1(ipid)) '/EB00' num2str(IDlist_1(ipid)) '_task1_000' num2str(irun) '.csv'];
%         csvwrite(output_name, data); 
%         clear('data');
%         
%     end
%     %Task2 (source memory)
%     %Load each mat file
%     fileload = [biopacmat_dir '00' num2str(IDlist_1(ipid)) '/EB00' num2str(IDlist_1(ipid)) '_task2_0000.mat'];
%     load(fileload);
%         
%     %write each mat file into csv
%     output_name = [out_dir '00' num2str(IDlist_1(ipid)) '/EB00' num2str(IDlist_1(ipid)) '_task2_0000.csv'];
%     csvwrite(output_name, data); 
%     clear('data');
%         
%     %Task 3 (volle task)
%     %Load each mat file
%     fileload = [biopacmat_dir '00' num2str(IDlist_1(ipid)) '/EB00' num2str(IDlist_1(ipid)) '_task3_0000.mat'];
%     load(fileload);
%         
%     %write each mat file into csv
%     output_name = [out_dir '00' num2str(IDlist_1(ipid)) '/EB00' num2str(IDlist_1(ipid)) '_task3_0000.csv'];
%     csvwrite(output_name, data); 
%     clear('data');
% end

%for participants 10-99
runNum = 7; % 6 runs in total
%only include normal participant's ID
%IDlist_2 = [10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30, 31, 33, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69];
% IDlist_2 = [35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69];
IDlist_2 = [45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69];
for ipid = 1:length(IDlist_2)
    for irun=2:runNum
        %Load each mat file
        fileload = [biopacmat_dir '0' num2str(IDlist_2(ipid)) '/EB0' num2str(IDlist_2(ipid)) '_task1_000' num2str(irun) '.mat'];
        load(fileload);
        %Create output directory
        outputdir = [out_dir '0' num2str(IDlist_2(ipid))];
        % Check if the folder exists
        if ~exist(outputdir, 'dir')
            % If the folder doesn't exist, create it
            mkdir(outputdir);
        end
        %write each mat file into csv
        output_name = [out_dir '0' num2str(IDlist_2(ipid)) '/EB0' num2str(IDlist_2(ipid)) '_task1_000' num2str(irun) '.csv'];
        csvwrite(output_name, data); 
        clear('data');
    end
    %Task2 (source memory)
    %Load each mat file
    fileload = [biopacmat_dir '0' num2str(IDlist_2(ipid)) '/EB0' num2str(IDlist_2(ipid)) '_task2_0000.mat'];
    load(fileload);
        
    %write each mat file into csv
    output_name = [out_dir '0' num2str(IDlist_2(ipid)) '/EB0' num2str(IDlist_2(ipid)) '_task2_0000.csv'];
    csvwrite(output_name, data); 
    clear('data');
        
    %Task 3 (volle task)
    %Load each mat file
    fileload = [biopacmat_dir '0' num2str(IDlist_2(ipid)) '/EB0' num2str(IDlist_2(ipid)) '_task3_0000.mat'];
    load(fileload);
        
    %write each mat file into csv
    output_name = [out_dir '0' num2str(IDlist_2(ipid)) '/EB0' num2str(IDlist_2(ipid)) '_task3_0000.csv'];
    csvwrite(output_name, data); 
    clear('data');
end