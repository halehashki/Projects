function covarience_coefficient()


networks={'0.1','0.01','0.5'}
for j=1:3
    
    j
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/R0_new/Watts/MD_10/Networks_',networks{j});
  
 for i=0:19
     i
    path=strcat(name,'/Network',int2str(i),'.txt');
    
    A=dlmread(path);
    
    
    
    
H=sum(A);
u=unique(H);
count=histc(H,unique(H));
p=count/1000; %size(R1,2);
k=u*p';
u2=u-1;
u3=u2.*u;
k2=u3*p';


 

d = sum(A,2); % degree of each node
cn = diag(A*triu(A)*A); % number of triangles for each node
c = zeros(size(d));
c(d>1) = 2*cn(d>1)./(d(d>1).*(d(d>1)-1));
%cc = sum(c.*d)/sum(d); % clustering coefficient 1
cc = mean(c(d>1));

t=[u count k k2 cc] ;

path3= strcat(name,'/CC','/Result',int2str(i),'.txt');

dlmwrite(path3,t);
 end
end


end