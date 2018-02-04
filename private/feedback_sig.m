%     ____            _       ______ _         ____   _____ _____
%    |  _ \          (_)     |  ____| |       |  _ \ / ____|_   _|
%    | |_) |_ __ __ _ _ _ __ | |__  | |_   _  | |_) | |      | |
%    |  _ <| '__/ _` | | '_ \|  __| | | | | | |  _ <| |      | |
%    | |_) | | | (_| | | | | | |    | | |_| | | |_) | |____ _| |_
%    |____/|_|  \__,_|_|_| |_|_|    |_|\__, | |____/ \_____|_____|
%                                       __/ |
%                                      |___/
%
% This functions is used to record and process online data it receives
% from the buffer. It generates a class label (-1 or 1) as a prediction 
% from the classifier specified. It finds the current path structure,
% connects to the buffer. Afterwards a selection dialog promts fro the user 
% to select a pre-trained classifier. Once done it starts recording data 
% according to the predefined instructions. After receiving the exit event
% (as soon as data is available in that case) a classifier calssifies the 
% input data and generates a label. Those labels are directly used to
% control the space ship for which reason they are translated to -1 or 1 in
% order to modify the ships x-axis movement.
%
% default settings:
%
% trlen_samp = 250; which corresponds to 1s of data in the present 
%                                           case (sampling rate of 250Hz)

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
[clsfra,path]=uigetfile([pwd filesep filesep '..' filesep 'classifiers' filesep '*.mat']);
clsfr=load([path,clsfra])
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