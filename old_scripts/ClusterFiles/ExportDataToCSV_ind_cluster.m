clear;
biopacmat_dir = '/zwork/jingyi/EB/EBpsychopyz_NegNeu/rawdata/EB_Psy_data/';
out_dir = '/zwork/jingyi/EB/EBpsychopyz_NegNeu/rawdata_sorted/';

% %for participants 6-9
% %only include normal participant's ID
% IDlist_1 = [8];
% runNum = 8; % 6 runs in total
% %pids = 9; %last PID in list
% i=2;
% for ipid = 1:length(IDlist_1)
%     for irun=3:runNum
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
%         output_name = [out_dir '00' num2str(IDlist_1(ipid)) '/EB00' num2str(IDlist_1(ipid)) '_task1_000' num2str(i) '.csv'];
%         csvwrite(output_name, data); 
%         clear('data');
%         i=i+1;
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
runNum = 6; % 6 runs in total
%only include normal participant's ID
% IDlist_2 = [15, 21, 27, 32, 68];
IDlist_2 = [40];
i=2;
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
        output_name = [out_dir '0' num2str(IDlist_2(ipid)) '/EB0' num2str(IDlist_2(ipid)) '_task1_000' num2str(i) '.csv'];
        csvwrite(output_name, data); 
        clear('data');
          i=i+1;
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