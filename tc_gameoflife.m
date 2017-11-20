function grid_out=tc_gameoflife(varargin)
if size(varargin{1},2)<2 && mod(varargin{1}(1),1)==0
    gridsize=varargin{1};
    grid_=zeros(gridsize);
    god=0.001;
    num_start_clusters=round(gridsize)/10;
    clustersize=round(gridsize)/20;
    clustercomplexity=0.1;
    
    for n=1:num_start_clusters
        randclust=zeros(ceil((round(rand*clustersize+1))));
        randclust(rand(size(randclust))>clustercomplexity)=1;
        size_clust=size(randclust,1);
        randloc=round(rand(1,2).*(gridsize-size_clust-2))+1;
        randindclust=sub2ind(size(grid_),repmat(randloc(1):randloc(1)+size_clust-1,size_clust,1),repmat((randloc(2):randloc(2)+size_clust-1)',1,size_clust));
        grid_(randindclust)=randclust;
    end
    
    s=size(grid_);
    N=length(s);
    [c1{1:N}]=ndgrid(1:3);
    c2(1:N)={2};
    
else
    gridsize=size(varargin{1},2);
    god=0.0001;
    
    grid_=varargin{1};
    s=size(grid_);
    N=length(s);
    [c1{1:N}]=ndgrid(1:3);
    c2(1:N)={2};
    
end

alifeind=find(grid_)';
old_grid=grid_;
for n=alifeind
    offsets=(sub2ind(s,c1{:}) - sub2ind(s,c2{:}));
    tmptmpind=n+offsets;
    tmptmpind(tmptmpind>(gridsize^2))=[];
    tmptmpind(tmptmpind<1)=[];
    neighbors = old_grid(tmptmpind);
    SN=sum(neighbors(:));
    %%% 1-3 rule: all <2 neighbors die %%%
    if SN<3 || SN > 4 || rand<god % so all together there need to be 3-4 persons in one block
        grid_(n)=0;
    end
    tmpind=n+offsets;
    tmpind(tmpind>(gridsize^2))=[];
    tmpind(tmpind<1)=[];
    %%% rule 4: all dead cells having 3 living neighbors become alive
    for m=tmpind(:)' % we only check dead cells around living to save ressources
        tmptmpind=m+offsets;
        tmptmpind(tmptmpind>(gridsize^2))=[];
        tmptmpind(tmptmpind<1)=[];
        neighbors = old_grid(tmptmpind);
        if sum(neighbors(:))==3 || rand<god
            grid_(m)=1;
        end
    end
    
end
grid_out=grid_;
end