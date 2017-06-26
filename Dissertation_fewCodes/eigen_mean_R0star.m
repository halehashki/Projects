function F=eigen_mean_R0star()   %%%%Beta,gamma,n

names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};

for k=1:3
    k
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{k},'/Networks2');
  
     %%% name=('/Users/halehashki/Haleh/Thesis/Paper/codes/data/watts_strogatz_Network/Networks4');
% parfor i=1:49
%    
%    
%     path=strcat(name,'/Eigenvalue/Result',int2str(i),'.txt');
%    
%     A=dlmread(path);
%    
%     E(:,i)=A;
%     
%   
%     
% end
% M=mean(E,2);
% path2=strcat(name,'/Eigenvalue/Eig_mean.txt');
% dlmwrite(path2,M);
%     



path2=strcat(name,'/Eigenvalue/Eig_mean.txt');

path2
s=dlmread(path2);

for j=1:size(s,1)-1
    e(j)=abs(s(j+1)-s(j));
end

m=1;
while (e(m))  > .005   %.005
    m=m+1;

end


m=m-1;
d=(s(m)-s(1))/(m-1);

t=[m d]
F(k,:)=t;


end





end