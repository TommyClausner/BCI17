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


CLASSIFIER_PATH = [pwd filesep '..' filesep 'classifiers'];
DATA_PATH = [pwd filesep '..' filesep '0001'];

trlen_ms=1000;
[data,devents,hdr,allevents] = sliceraw(DATA_PATH,'startSet',{'stim.target'},'trlen_ms',trlen_ms);

d = dir(CLASSIFIER_PATH); %look up saved classifiers
d = d(3:end); %first two entries are '.' and '..'

%Create labels
Y = {devents.value};
numY = ones(1,length(Y));
numY(find(strcmp(Y,'2 RH'))) = -1;

%Apply all saved classifiers to data
preds = zeros(length(d),length(data));
for i = 1:length(d)
	clsfr = load([CLASSIFIER_PATH filesep 'clsfr' num2str(i) '.mat']);
	preds(i,:) = buffer_apply_clsfr(data,clsfr);
	fprintf('Clsfr perf = %g\n',sum(sign(preds(i,:))==numY)./numel(preds(i,:)))
end

%Take mean prediction
mean_pred = mean(preds,1);
fprintf('Mean clsfr perf = %g\n',sum(sign(mean_pred)==numY)./numel(mean_pred))
