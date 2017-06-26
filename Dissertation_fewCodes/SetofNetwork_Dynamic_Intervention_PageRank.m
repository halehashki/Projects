function [N]=SetofNetwork_Dynamic_Intervention_PageRank(A,invtime,nodenumber,immunization)    %% N= new...    %%n: number of nodes   t:number of time steps

%%path='Users/halehashki/Haleh/Thesis/Paper/codes/data/barabasi_albert_Network/Networks2/Dynamic_Netwrok/Network1';
t=1000;

A=wighted_matrix(A);

n=size(A,1);
TH=.9;
TH_recovered=0.9;


L=zeros(n,1);
L(:,1)= .05;



%%% random node whicih is infected first
r=round(1 + (n-1).*rand(1,1));


XI=zeros(n,1);
XR=ones(n,1);
XR=0.000001*XR;

FIR=zeros(n,2);  %%% Infected, recoverd



N=zeros(t,2);

counter=1;
XI(r)=1;
FIR(r,1)=1;
DXI=zeros(n,1);

N(counter,1)=1;


time=[20,60,90,120,200];

for i=1:t    
    
  if i ==  time(1) ||  i ==  time(2) || i ==  time(3) || i ==  time(4) || i ==  time(5) 
        
        A=make_reduce_matrix(A);
        
        
  elseif i == invtime
   
        nodes=eig_vector(A,nodenumber);
        A=intervention(A, nodes,immunization);
       
       
   end



% if i == invtime
%    mean(mean(A,2))
%         nodes=eig_vector(A,nodenumber);
%         A=intervention(A, nodes);
%        
%        mean(mean(A,2))
%    end


   
    ind1=find(XI >= TH  & XI < 1);
    %%% disconnect the edges
    
        A(ind1,:)=0;
        A(:,ind1)=0;
   
    
    DXI=A*XI;
    
    DXR=zeros(size(XR));
    for j=1:n
        if FIR(j,1) == 1 
            DXI(j,1)=0; 
            
            if FIR(j,2) ~= 1
            
            DXR(j,1)=(L(j,1)*XR(j,1));
            
            end
            
           
        end    
    end
    
    
    
    
    
    %
    XI=XI+DXI;
    XR=XR+DXR;
    %XS=1-(XI+XR);
    
%     X(:,i)=XI(10);
%      Y(:,i)=DXI(10);
    
    
    
    
    ind1=find(XI >= TH);   %%% bigger than threshold
    FIR(ind1,1)=1;
    
    
    %%%just for test
    ind1=find(XR >= TH_recovered);   %%% bigger than threshold
    FIR(ind1,2)=1;
    
    
    
    
    
    
    ind1=find(FIR(:,1) == 1); %%% & FIR(:,2) == 0);  %%infected
    ind2=find(FIR(:,2) == 1); %%recovered
   % ind3=find(FIR(:,1) == 0); %% susceptible
    
    inf=size(ind1,1);
    rec=size(ind2,1);
    %sus=size(ind3,1);
    
    
    
    N(i,1)=inf;
    N(i,2)=rec;
    %N(i,3)=sus;
    
    
   
end

end

function A=intervention(A, nodes,immunization)
%%% reduce the weighte of targeted nodes by 60%

for i=1:size(nodes,1)
    t=A(nodes(i),:);
    t=t-(immunization*t);  %immunization=0.6
    A(nodes(i),:)=t;
    
    
    t=A(:,nodes(i));
    t=t-(immunization*t);
    A(:,nodes(i))=t;

 
end    




end


function nodes=eig_vector(A,number)
 d  = 0.85;
n=size(A,1);
OutLinks = sum(A,1);

  M = zeros(n,n);

  for i = 1:n
    M(:,i) = A(:,i)/OutLinks(i);
  end
  
  
  
  clear OutLinks;
  

    R    = 1/n*ones(n,1);
    R    = R ./ norm(R, 2);
    
    last_R = ones(n, 1) * inf;
    Mhat   = d*M + ((1-d)/n)*ones(n,n); 
 
    while(norm(R - last_R, 2) > 1e-4)
      last_R = R;
      R = Mhat * R;
      R = R ./ norm(R, 2);
    end



[va nodes]=sort(R,'descend');
nodes=nodes(1:number*10);
size(find(nodes));




end

function A=wighted_matrix(A)

%n=size(A,1);
%%% using sparse command to reduce memory and increase efficency
% [i,j,s] = find(A);
% [m,n] = size(A);
% A = sparse(i,j,s,m,n);

% W=ones(n,1);
% W=.005 * W; %% ; %.005; 
W = normrnd(0.005,0.001,1000,1);

P=zeros(size(A));   %%% making new matrix which get lots of memory , may just replace in A.I did not that to be able to change the W or A matrix later
for i=1:size(W,1)
    P(i,:)=W(i,1)*A(i,:);
end


A=P;
clear P;
end


function A=make_reduce_matrix(A)
n=50; %% reduce degree of n nodes by p percentage
p=40;
nodes=randsample(size(A,2),n);  %% random nodes to reduce their degree
for i=1:n
    
    nonzero=find(A(nodes(i),:)); 
    d=size(nonzero,2);%% degree of each node
    dif = round(d .* (p/100)) ; %% reduce by p%
    if dif >0 
    
    %%nonzero=find(A(nodes(i),:));
    y = randsample(nonzero,dif); %% randomly chose nodes to diconnect them
    
    
    for j=1:size(y,2)
         
        
         A(nodes(i),y(j))=0;
         A(y(j),nodes(i))=0;
    end
    end    

end
end