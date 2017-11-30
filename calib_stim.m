%%
clc
clear
close all
rawpath='/Users/Tommy/Documents/Nijmegen/Study/BCI/buffer_bci-master';

matlab_path=[rawpath '/matlab'];
tut_path=[rawpath '/tutorial'];
cd([tut_path '/lect4-im'])

try; cd(fileparts(mfilename('fullpath')));catch; end;
try;
    run ../../matlab/utilities/initPaths.m
catch
    msgbox({'Please change to the directory where this file is saved before running the rest of this code'},'Change directory');
end

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

clc
clear
rng('shuffle')
grid_=tc_gameoflife(100);
s_=size(grid_,1);
arrow_size=round(s_/8);

close all
figure
clf
set(gcf,'visible','off','toolbar','none','menubar','none','color','k','Units','normalized','Position',[0 0 1 1],'Renderer','OpenGL','RendererMode','manual'); % black figure
GoL=imagesc(grid_);
colormap gray
right_arrow=patch('vertices',[0,0;0,arrow_size;arrow_size,arrow_size/2],'faces',[1,2,3],'edgecolor','none','facecolor','r');
left_arrow=patch('vertices',[0,0;0,arrow_size;-arrow_size,arrow_size/2],'faces',[1,2,3],'edgecolor','none','facecolor','b');

xlim([1 s_])
ylim([-s_*0.1-arrow_size s_])

offset_X=round(s_*0.25)+1;
offset_Y=round(s_*0.1)+1;

line(xlim,[0 0],'color','w')
axis off
hold off
set(gca,'YDir','normal')

left_arrow.Vertices(:,1)=left_arrow.Vertices(:,1)+offset_X;
right_arrow.Vertices(:,1)=right_arrow.Vertices(:,1)+offset_X+s_/2-round(s_/16);

left_arrow.Vertices(:,2)=left_arrow.Vertices(:,2)-s_/5;
right_arrow.Vertices(:,2)=right_arrow.Vertices(:,2)-s_/5;

stim_one_freq=8;
stim_two_freq=16;

stim_two_freqUDGoL=32;

delay_one=1/stim_one_freq;
delay_two=1/stim_two_freq;
delay_GoL=1/stim_two_freqUDGoL;

instr=text(s_/2*0.95,(-s_*0.1-arrow_size)/2,'+','color','w','fontsize',64);

trial_time=1;
instrstrings={'<','+','>'};


vis_figT = timer('Period',1,... %period
    'ExecutionMode','singleShot',... %{singleShot,fixedRate,fixedSpacing,fixedDelay}
    'BusyMode','queue',... %{drop, error, queue}
    'TasksToExecute',1,...
    'StartDelay',1,...
    'TimerFcn',@(src,evt)set(gcf,'visible','on'),...
    'StartFcn',[],...
    'StopFcn',[],...
    'ErrorFcn',[]);
TV2 = timer('Period',delay_two,... %period
    'ExecutionMode','fixedRate',... %{singleShot,fixedRate,fixedSpacing,fixedDelay}
    'BusyMode','drop',... %{drop, error, queue}
    'TasksToExecute',inf,...
    'StartDelay',0+0.002,...
    'TimerFcn',@(src,evt)set(left_arrow,'facecolor','b'),...
    'StartFcn',[],...
    'StopFcn',[],...
    'ErrorFcn',[]);
TI2 = timer('Period',delay_two,... %period
    'ExecutionMode','fixedRate',... %{singleShot,fixedRate,fixedSpacing,fixedDelay}
    'BusyMode','drop',... %{drop, error, queue}
    'TasksToExecute',inf,...
    'StartDelay',delay_two/2+0.003,...
    'TimerFcn',@(src,evt)set(left_arrow,'facecolor','k'),...
    'StartFcn',[],...
    'StopFcn',[],...
    'ErrorFcn',[]);
TV1 = timer('Period',delay_one,... %period
    'ExecutionMode','fixedRate',... %{singleShot,fixedRate,fixedSpacing,fixedDelay}
    'BusyMode','drop',... %{drop, error, queue}
    'TasksToExecute',inf,...
    'StartDelay',0+0.005,...
    'TimerFcn',@(src,evt)set(right_arrow,'facecolor','r'),...
    'StartFcn',[],...
    'StopFcn',[],...
    'ErrorFcn',[]);
TI1 = timer('Period',delay_one,... %period
    'ExecutionMode','fixedRate',... %{singleShot,fixedRate,fixedSpacing,fixedDelay}
    'BusyMode','drop',... %{drop, error, queue}
    'TasksToExecute',inf,...
    'StartDelay',delay_one/2+0.007,...
    'TimerFcn',@(src,evt)set(right_arrow,'facecolor','k'),...
    'StartFcn',[],...
    'StopFcn',[],...
    'ErrorFcn',[]);
TGOL = timer('Period',delay_GoL,... %period
    'ExecutionMode','fixedRate',... %{singleShot,fixedRate,fixedSpacing,fixedDelay}
    'BusyMode','drop',... %{drop, error, queue}
    'TasksToExecute',inf,...
    'StartDelay',0+0.011,...
    'TimerFcn',@(src,evt)set(GoL,'CData',tc_gameoflife(get(GoL,'CData'))),...
    'StartFcn',[],...
    'StopFcn',[],...
    'ErrorFcn',[]);
TLT = timer('Period',trial_time,... %period
    'ExecutionMode','fixedRate',... %{singleShot,fixedRate,fixedSpacing,fixedDelay}
    'BusyMode','drop',... %{drop, error, queue}
    'TasksToExecute',inf,...
    'StartDelay',0+0.013,...
    'TimerFcn',@(src,evt) cellfun(@(x)feval(x,src,evt),...
    {@(src,evt)set(instr,'String',instrstrings{randi(3)}),...
    @(src,evt)sendEvent('stim.stim',find([instrstrings{:}]==get(instr,'String')))},'unif',0),...
    'StartFcn',[],...
    'StopFcn',[],...
    'ErrorFcn',[]);

start(TV2);start(TI2);start(TV1);start(TI1);

start(TGOL);

start(TLT);

start(vis_figT);

waitfor(gcf)
delete(timerfind)