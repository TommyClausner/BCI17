%     ____            _       ______ _         ____   _____ _____
%    |  _ \          (_)     |  ____| |       |  _ \ / ____|_   _|
%    | |_) |_ __ __ _ _ _ __ | |__  | |_   _  | |_) | |      | |
%    |  _ <| '__/ _` | | '_ \|  __| | | | | | |  _ <| |      | |
%    | |_) | | | (_| | | | | | |    | | |_| | | |_) | |____ _| |_
%    |____/|_|  \__,_|_|_| |_|_|    |_|\__, | |____/ \_____|_____|
%                                       __/ |
%                                      |___/
%
% This functions is used to call the buffer's default signal viewer
% It is only a wrapper function that finds the current path structure,
% connects to the buffer and launches the signal viewer (sigViewer.m)

clc
clear
close all
try;run([pwd filesep filesep '..' filesep 'external' filesep 'matlab' filesep 'utilities' filesep 'initPaths.m']);end

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
%capFitting;
sigViewer(buffhost,buffport)
exit