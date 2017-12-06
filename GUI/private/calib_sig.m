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

trlen_ms=4000;

[data,devents,state]=buffer_waitData(buffhost,buffport,[],'startSet',{'stim.target'},'exitSet',{'stim.training' 'end'},'trlen_ms',trlen_ms);
devents(end,:)=[]; % removing last devent entry due to the exit event
data(end,:)=[]; % removing last data entry due to the exit event

clsfr=buffer_train_ersp_clsfr(data,devents,hdr,'spatialfilter','CAR','freqband',[0.1 1 30 31],'badtrrm',0,'badchrm',0,'capFile','1010');

save clsfr clsfr
waitfor(gcf)
exit