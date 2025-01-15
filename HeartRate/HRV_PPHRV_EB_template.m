%Created by Jingyi Wang, May 8 2024
%PPHRV package tutorial: http://users.neurostat.mit.edu/barbieri/pphrv
clear all;
close all;

sub=replaceSUB
run=replaceRUN

outdir1 = '/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/HRV_processed/';
%Load data
disp(['/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/EKG_processed/' sub '_encodingEKG_ECode_' num2str(run) '.csv'])
data = load(['/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/EKG_processed/' sub '_encodingEKG_ECode_' num2str(run) '.csv']);
outdir = [outdir1 sub];
if ~exist(outdir, 'dir')
    % If the folder doesn't exist, create it
    mkdir(outdir);
end
%TimePoint = data(:, 2);
%RR = data(:, 1);
R = data(:,1); % series of times of R-events [s]

%Get timepoints that only contain event code
EventCode = data(:,2); %series of event codes
ECtimes = data(:,3); %series of timepoints for event codes
% Logical indexing to filter rows where the second column's value is larger than 0
filtered_rows = EventCode > 0;

% Get the values from the third column where the condition is satisfied
ECtimes_cleaned = ECtimes(filtered_rows);
EventCode_cleaned = EventCode(filtered_rows);

%plot(TimePoint, RR) % [ms]
%xlabel('time [s]')
%ylabel('RR [ms]')

figure;hold on
plot(R(2:end), 1000*diff(R)) % [ms]
xlabel('time [s]')
ylabel('RR [ms]')
% Save the figure as a JPG image
outfn = [outdir '/TimevsRR' num2str(run) '.jpg']
saveas(gcf, outfn, 'jpg');

%find the parameters of a history-dependent inverse Gaussian (IG) distribution by maximizing the likelihood.
%perform Inverse Gaussian regression
[Thetap,Kappa,opt] = regr_likel(R);

%Get the powder spectral density
meanRR = mean(diff(R)); % average RR interval
Var = meanRR^3 / Kappa; % variance of an inverse Gaussian
Var = 1e6 * Var; % from [s^2] to [ms^2]
spectral(Thetap, Var, 1/meanRR);
% with Thetap: coeffs of IG regression; Var: variance; 1/meanRR: sampling freq
xlabel('f [Hz]')
ylabel('PSD [ms^2/Hz]')
% Save the figure as a JPG image
outfn = [outdir '/powerSpectrum' num2str(run) '.jpg']
saveas(gcf, outfn, 'jpg');

%Point-process assessment of time-varying HRV indices through local likelihood of IG distribution
R = data(:,1); % series of times of R-events [s]
[Thetap,Mu,Kappa,L,opt] = pplikel(R);
t = opt.t0 + (0:length(Mu)-1) * opt.delta;
Var = opt.meanRR.^3 ./ Kappa; % variance of an inverse Gaussian
Var = 1e6 * Var; % from [s^2] to [ms^2]
figure; hold on
plot(R(2:end), 1000*diff(R), 'r*')
plot(t, 1000*Mu)
legend('RR', 'First moment of IG distribution')
xlabel('time [s]')
ylabel('[ms]')
% Save the figure as a JPG image
outfn = [outdir '/IGdistribution' num2str(run) '.jpg']
saveas(gcf, outfn, 'jpg');

%Get the time-varying power of LF, power of LF/HF index
[powLF, powHF, bal] = hrv_indices(Thetap, Var, 1./opt.meanRR);

figure
plot(t, powLF)
%Draw event onsets
%Make ECtimes_clean vector as the same length as t/powLF for plotting purpose. 
ECtimes_powLFext = zeros(1, length(powLF));
ECtimes_powLFext(1:length(ECtimes_cleaned)) = ECtimes_cleaned;

%EventCode_powLFext = ECtimes_powLFext;
%positive_values = EventCode_powLFext(EventCode_powLFext > 0);
%EventCode_powLFext(1:length(positive_values)) = EventCode_cleaned;

%plot
hold on
plot([ECtimes_powLFext; ECtimes_powLFext], [0; max(powLF)], 'r-');  % 'r--' specifies red dashed lines
xlabel('t [s]'); ylabel('powLF');
% Save the figure as a JPG image
outfn = [outdir '/powLF' num2str(run) '.jpg'];
saveas(gcf, outfn, 'jpg');
% saveas(gcf, '/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/powLF.jpg', 'jpg');

figure
plot(t, powHF)
%plot
hold on
plot([ECtimes_powLFext; ECtimes_powLFext], [0; max(powHF)], 'r-');  % 'r--' specifies red dashed lines
xlabel('t [s]'); ylabel('powHF');
% Save the figure as a JPG image
outfn = [outdir '/powHF' num2str(run) '.jpg']
saveas(gcf, outfn, 'jpg');
% saveas(gcf, '/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/powHF.jpg', 'jpg');

figure
plot(t, bal)
%plot
hold on
plot([ECtimes_powLFext; ECtimes_powLFext], [0; max(bal)], 'r-');  % 'r--' specifies red dashed lines
xlabel('t [s]'); ylabel('LF/HF'); ylim([-1, 20])
% Save the figure as a JPG image
outfn = [outdir '/powLFvsHF' num2str(run) '.jpg']
saveas(gcf, outfn, 'jpg');
% saveas(gcf, '/zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/powLFvsHF.jpg', 'jpg');

%Use Eventcode time to create Eventcode column
EventCode_indx = [];

%Create EventCode_powLFext vector
EventCode_powLFext = zeros(1, length(powLF));
EventCode_Times = zeros(1,length(powLF));
%Find the indices of elements in t that are also in ECtimes_cleaned
[~, EventCode_indx] = ismember(ECtimes_cleaned, t);

j=1;
for i = 1:numel(EventCode_indx)
	indtmp = EventCode_indx(i);
    disp(indtmp);
	if indtmp==0
		%find the ECtime that is not equal to any time points
		b = ECtimes_cleaned(j)
		% Calculate the absolute differences between each element in the t and 'b'
		abs_diff = abs(t - b);

		% Find the index of the element with the minimum absolute difference
		[~, idx] = min(abs_diff);
        disp(idx);
		EventCode_powLFext(idx) = EventCode_cleaned(j);
        EventCode_Times(idx) = ECtimes_cleaned(j);
    	j = j+1;
		
	else
    	EventCode_powLFext(indtmp) = EventCode_cleaned(j);
        EventCode_Times(indtmp) = ECtimes_cleaned(j);
    	j = j+1;
    end
end

%Create table from vectors
dataMatrix = [t', powLF', powHF', bal', EventCode_Times', EventCode_powLFext'];
T = array2table(dataMatrix, 'VariableNames', {'timepoints', 'powLF', 'powHF', 'powLFvsHF', 'ECtimes', 'EventCode'});

% Save the table to a file with header names
outfn = [outdir '/' sub '_encodingEKG_ECode_' num2str(run) '_processed.csv']
writetable(T, outfn);

