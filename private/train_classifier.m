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
DATA_PATH = [pwd filesep '..' filesep '0001'];

cap_=uigetfile([pwd filesep filesep '..' filesep 'external' filesep 'resources' filesep 'caps' filesep '*.txt']);
cap_=cap_(1:end-4);

trlen_ms=2000;

[data,devents,hdr,allevents] = sliceraw(DATA_PATH,'startSet',{'stim.target'},'trlen_ms',trlen_ms);
[clsfr,res,X,Y]= buffer_train_ersp_clsfr(data,devents,hdr,'spatialfilter','CAR','freqband',[0.1 1 30 31],'badtrrm',0,'badchrm',0,'capFile',cap_,'overridechnms',1);

num = numel(dir([CLASSIFIER_PATH filesep '*.mat'])) + 1;
save([CLASSIFIER_PATH filesep 'clsfr' num2str(num)],'-struct','clsfr');

