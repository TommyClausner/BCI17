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