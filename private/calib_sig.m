%     ____            _       ______ _         ____   _____ _____
%    |  _ \          (_)     |  ____| |       |  _ \ / ____|_   _|
%    | |_) |_ __ __ _ _ _ __ | |__  | |_   _  | |_) | |      | |
%    |  _ <| '__/ _` | | '_ \|  __| | | | | | |  _ <| |      | |
%    | |_) | | | (_| | | | | | |    | | |_| | | |_) | |____ _| |_
%    |____/|_|  \__,_|_|_| |_|_|    |_|\__, | |____/ \_____|_____|
%                                       __/ |
%                                      |___/
%
% This functions is used to record and process calibration data it receives
% from the buffer. It finds the current path structure,
% connects to the buffer. Afterwards a selection dialog promts fro the user 
% to select the respective EEG cap. Once done it starts recording data 
% according to the predefined instructions. After receiving the exit event 
% a classifier is trained on that data. Output data is saved in /output and 
% classifier results in /classifier
%
% default settings:
%
% trlen_ms=2000;
% spatialfilter = 'CAR'
% freqband = [0.1 1 30 31]
% badchrm = 0
% badtrrm = 0

clc
clear
close all

try;run([pwd filesep filesep '..' filesep 'external' filesep 'matlab' filesep 'utilities' filesep 'initPaths']);end

buffhost='localhost';buffport=1972;
% wait for the buffer to return valid header information
hdr=[];
while ( isempty(hdr) || ~isstruct(hdr) || (hdr.nchans==0) ) % wait for the buffer to contain valid data
  try 
    hdr=buffer('get_hdr',[],buffhost,buffport); 
  catch
    hdr=[];
    fprintf('Invalid header info... waiting.\n');
  end;
  pause(1);
end;

CLASSIFIER_PATH = ['..' filesep 'classifiers'];
DATA_PATH = ['..' filesep 'output']

cap_=uigetfile([pwd filesep filesep '..' filesep 'external' filesep 'resources' filesep 'caps' filesep '*.txt']);
cap_=cap_(1:end-4);

% length of data that is recorded
trlen_ms=2000;

sendEvent('calib.start',1)
[data,devents,state]=buffer_waitData(buffhost,buffport,[],'startSet',{'stim.target'},'exitSet',{'stim.training' 'end'},'trlen_ms',trlen_ms);
devents(end,:)=[]; % removing last devent entry due to the exit event
data(end,:)=[]; % removing last data entry due to the exit event

clsfr=buffer_train_ersp_clsfr(data,devents,hdr,'spatialfilter','CAR','freqband',[0.1 1 30 31],'badtrrm',0,'badchrm',0,'capFile',cap_,'overridechnms',1);

num = numel(dir([CLASSIFIER_PATH filesep '*.mat'])) + 1;
save([CLASSIFIER_PATH filesep 'clsfr' num2str(num)],'-struct','clsfr');

save_data.data = data;
save_data.devents = devents;
num = numel(dir([DATA_PATH filesep '*.mat'])) + 1;
save([DATA_PATH filesep 'data' num2str(num)],'-struct','save_data');

waitfor(gcf)
exit