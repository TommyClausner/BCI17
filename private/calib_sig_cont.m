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

CLASSIFIER_PATH = ['..' filesep 'classifiers'];

cap_=uigetfile([pwd filesep filesep '..' filesep 'external' filesep 'resources' filesep 'caps' filesep '*.txt']);
cap_=cap_(1:end-4);

trlen_ms=1000;%samples
state=hdr;

while true
	[data,devents,state]=buffer_waitData(buffhost,buffport,state,'startSet',{'stim.target'},'trlen_samp',trlen_ms,'exitSet',{'data' 'stim.training' 'end'});
	if ( matchEvents(devents(end),'stim.training','end') )
		break
	end
	if(~exist('all_data'))
		all_data = data;
		all_devents = devents;
	else
		all_data = [all_data data];
		all_devents = [all_devents devents];
	end

	if(mod(size(all_data,2),10) == 0)
		%retrain classifier
		[clsfr,res,X,Y] = buffer_train_ersp_clsfr(all_data,all_devents,hdr,'spatialfilter','CAR','freqband',[0.1 1 30 31],'badtrrm',0,'badchrm',0,'capFile',cap_,'overridechnms',1,'visualize',0);
		f = res.opt.tstf; %predictions
		pred = (f>0)*2-1; %predicted classes
		numY = ones(1,length(Y));
		numY(find(strcmp(Y,'1 LH'))) = -1;
		fprintf('Clsfr perf = %g\n',sum(pred==numY')./numel(pred)) %print accuracy
	end
end

num = numel(dir([CLASSIFIER_PATH filesep '*.mat'])) + 1;
save([CLASSIFIER_PATH filesep 'clsfr' num2str(num)],'-struct','clsfr');
