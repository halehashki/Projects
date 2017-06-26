function [N]=SIR_Dynamic_Intervention(A,invtime,nodenumber)    %% N= new...    %%n: number of nodes   t:number of time steps
t=1000;

n=size(A,1);
%%% using sparse command to reduce memory and increase efficency
[i,j,s] = find(A);
[m,n] = size(A);
A = sparse(i,j,s,m,n);

W=ones(n,1);
W=.005 * W; %% ; %.005; 


P=zeros(size(A));   %%% making new matrix which get lots of memory , may just replace in A.I did not that to be able to change the W or A matrix later
for i=1:size(W,1)
    P(i,:)=W(i,1)*A(i,:);
end

A=P;


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

%%%%% intervention set up 
%%time=[30,60,90,120,200];



for i=1:t    
    %if i ==  time(1) ||  i ==  time(2) || i ==  time(3) || i ==  time(4) || i ==  time(5)
   if  i == invtime   
        nodes=eig_vector(A,nodenumber);
        A=intervention(A, nodes);
    end
    
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
    
    %%X(:,i)=XI(5);
    
    
    
    
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

function A=intervention(A, nodes)


  for i=1:size(nodes,1)
      A(i,:)=0;
      A(:,i)=0;
  end


end


function nodes=eig_vector(A,nodenumber)

% L=diag(sum(A))-A;
% [V E]=eig(L);
% [ES EI]=sort(diag(E),'descend');
% EH=V(:,EI(1));
% [va nodes]=sort(EH,'descend');  %% values and index of the sortes eigenvector of the largest eigenvale
% nodes=nodes(1:nodenumber*10); %%% 5% of nodes
% 
[V E]=eig(A);
[va nodes]=sort(V(:,size(A,1)),'descend');
nodes=nodes(1:nodenumber*10);


end