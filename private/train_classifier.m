clc
clear
close all

try;run([pwd filesep filesep '..' filesep 'external' filesep 'matlab' filesep 'utilities' filesep 'initPaths']);end

CLASSIFIER_PATH = ['..' filesep 'classifiers'];
DATA_PATH = [pwd filesep '..' filesep 'output' filesep 'Robert'];

cap_=uigetfile([pwd filesep filesep '..' filesep 'external' filesep 'resources' filesep 'caps' filesep '*.txt']);
cap_=cap_(1:end-4);

trlen_ms=2000;

%[data,devents,hdr,allevents] = sliceraw(DATA_PATH,'startSet',{'stim.target'},'trlen_ms',trlen_ms);
num = numel(dir([DATA_PATH filesep 'data*.mat']));
data = [];
devents = [];
for i=1:num
	all_data = load([DATA_PATH filesep 'data' num2str(i) '.mat']);
	data = [data; all_data.data];
	devents = [devents; all_data.devents];
end

[clsfr,res,X,Y]= buffer_train_ersp_clsfr(data, devents,[],'fs', 250, 'spatialfilter','CAR','freqband',[0.1 1 30 31],'badtrrm',0,'badchrm',0,'capFile',cap_,'overridechnms',1);

num = numel(dir([CLASSIFIER_PATH filesep 'clsfr_offline*.mat'])) + 1;
save([CLASSIFIER_PATH filesep 'clsfr_offline' num2str(num)],'-struct','clsfr');

