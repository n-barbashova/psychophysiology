clear;

%%% Cannot read file /Users/nadezhdabarbashova/Desktop/fmcc/data/sub03/fmcc_sub03_task_0000.mat.
 

% to use this file you need to first convert acq files into matlab files 

% folder with all files acq and mat 
biopacmat_dir = '/Users/nadezhdabarbashova/Desktop/fmcc/data';


% folder to export csv files to 
out_dir ='/Users/nadezhdabarbashova/Desktop/fmcc/data/fmcc_csv';
 
%for participants 6-9
runNum = 0:8; % 9 runs in total
pids = 5; % last participant id in list  

for ipid = 4:pids
    participant_id = sprintf('%02d', ipid);
    for irun= runNum 
        % Load each mat file 
        % mat files 
        participant_dir = fullfile(biopacmat_dir, sprintf('sub%s', participant_id));

        %fileload = [biopacmat_dir '0' num2str(ipid) '/EB00' num2str(ipid) '_task1_000' num2str(irun) '.mat'];
        fileload = fullfile(participant_dir, sprintf('fmcc_sub%s_task_%04d.mat', participant_id, irun));
    
        if ~isfile(fileload)
            fprintf('File does not exist: %s\n', fileload);
            continue; % Skip to the next iteration
        end
        
 
        load(fileload);
        % Create output directory
        outputdir = [out_dir '00' num2str(ipid)];
        % Check if the folder exists
        if ~exist(outputdir, 'dir')
            % If the folder doesn't exist, create it
            mkdir(outputdir);
        end
        %write each mat file into csv
        % output_name = [out_dir '00' num2str(ipid) '/EB00' num2str(ipid) '_task1_000' num2str(irun) '.csv'];
        output_name = fullfile(outputdir, sprintf('fmcc_sub_%s_%04d.csv', participant_id, irun));
        %csvwrite(output_name, data); 
        %writematrix(data, output_name);
        clear('data');
    end
end





% %for participants 10-99 ---? 
% runNum = 7; % 6 runs in total
% pids = 14; %last PID in list
% for ipid = 10:pids
%     for irun=2:runNum
%         %Load each mat file
%         fileload = [biopacmat_dir '0' num2str(ipid) '/EB0' num2str(ipid) '_task1_000' num2str(irun) '.mat'];
%         load(fileload);
%         %Create output directory
%         outputdir = [out_dir '0' num2str(ipid)];
%         % Check if the folder exists
%         if ~exist(outputdir, 'dir')
%             % If the folder doesn't exist, create it
%             mkdir(outputdir);
%         end
%         %write each mat file into csv
%         output_name = [out_dir '0' num2str(ipid) '/EB0' num2str(ipid) '_task1_000' num2str(irun) '.csv'];
%         csvwrite(output_name, data); 
%         clear('data');
%     end
% end

