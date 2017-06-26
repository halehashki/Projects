function [N]=SIR_Dynamic_adjacancy()    %% N= new...    %%n: number of nodes   t:number of time steps

D=42;
t=2160*D;
m=789;
n=789;



% A=dlmread('/Users/halehashki/Haleh/Thesis/Paper/codes/data/barabasi_albert_Network//Networks2/Networks/Network9.txt');
% W=ones(n,1);
% W=.005 * W; %% ; %.005; 
% 
% 
% P=zeros(size(A));   %%% making new matrix which get lots of memory , may just replace in A.I did not that to be able to change the W or A matrix later
% for i=1:size(W,1)
%     P(i,:)=W(i,1)*A(i,:);
% end
% 
% A=P;
% 



TH=.9;
TH_recovered=0.9;


L=zeros(n,1);
%L(:,1)=nthroot(TH_recovered/10E-6,t)-1
%L(:,1)=TH_recovered/(2160 * 20 * TH);
L(:,1)= .001;



%%% random node whicih is infected first
r=round(1 + (n-1).*rand(1,1));
di=round(1 + (13).*rand(1,1));



XI=zeros(n,1);
XR=ones(n,1);
XR=0.000001*XR;

FIR=zeros(n,2);  %%% Infected, recoverd


if di >1
    counter=(di-1) * 2160;
else
    counter=1;
end;


N=zeros(t,2);


XI(r)=1;
FIR(r,1)=1;
DXI=zeros(n,1);

N(counter,1)=1;
%N(1:counter,3)=n-1;




for d=di:D
    
    for i=195:2355    %%% 2160 steps equal to 12 hours
        counter=counter+1;
        
        
        
        if (mod(d,2) == 1  && ( d ~=  11   &&  d~= 13 &&  d~=25  && d ~=27  && d~=39 &&  d~=41 ))%%% it's odd and it's day
            
            if i == 789
                A=Make_Matrix(788);  %%% file 789 has an error so I read the previous file instead 
            else
                A=Make_Matrix(i);
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
            
            
        else   %%% at night just recovery is happening
            
            DXR=zeros(size(XR));
            for j=1:n
                 if FIR(j,1) == 1
                    if FIR(j,2) ~= 1
                    
                    DXR(j,1)=(L(j,1)*XR(j,1));
                    %DXR(j,1)=(L(j,1)*TH);
                    end
                 end 
            end
            
        end
        
        
        
        
        
        
    
    


%
XI=XI+DXI;
XR=XR+DXR;



ind1=find(XI >= TH);   %%% bigger than threshold
FIR(ind1,1)=1;


%%%just for test
ind1=find(XR >= TH_recovered);   %%% bigger than threshold
FIR(ind1,2)=1;






ind1=find(FIR(:,1) == 1); %%% & FIR(:,2) == 0);  %%infected
ind2=find(FIR(:,2) == 1); %%recovered

inf=size(ind1,1);
rec=size(ind2,1);



N(counter,1)=inf;
N(counter,2)=rec;

    end

end


end






function A=Make_Matrix(i)

m=789;
n=789;
beta=0.0003;
A=zeros(m,n);

filepath='/Users/halehashki/Haleh/Thesis/Research/salathe/moteFiles/TimeStamp/';
nodeid=strcat('Time',int2str(i));
filename=strcat(filepath,nodeid);
fid = fopen(filename);
fileind=fgets(fid);
if fileind == -1
    A=zeros(m,n);
    
    
else
    
    T= dlmread(filename);
    


R1=T(1,:);
R2=T(2,:);

s=ones(1,length(R1));
s=beta*s;
A = sparse(R1,R2,s,m,n);


% R1=T(1,:);
% R2=T(2,:);
% for j=1:size(R1,2)
% A(R1(j),R2(j))=beta;
% 
% end

end
fclose(fid);
end