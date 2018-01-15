%%
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
clsfr=uigetfile([pwd filesep filesep '..' filesep 'classifiers' filesep '*.mat']);
load(clsfr)
trlen_samp=250;%samples
state=hdr;

while true
[data,devents,state]=buffer_waitData(buffhost,buffport,state,'startSet',{'stim.target'},'trlen_samp',trlen_samp,'exitSet',{'data'});
if devents(end).value==0
    break
end
[f,fraw,p]=buffer_apply_ersp_clsfr(data.buf,clsfr);
sendEvent('classifier.prediction',(f>0)*2-1);
end
exit