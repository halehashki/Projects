function A=make_dynamic_reduced_degree_matrix()  
%% A : matrix n:number of nodes to reduce theri degree p: percentage to reduce node degree
n=10; %%% number of nodes to reduce their degree
p=40;  %% percentage to reduce the node degree

names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};




for j=2:3
    j
    for i=1:15
     i   
    name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Networks/Network', num2str(i),'.txt');
    A=dlmread(name);
    
    
    name2=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Dynamic_Netwrok/Network',num2str(i) ,'.txt');
    for k=1:6
      name2=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Dynamic_Netwrok/Network', num2str(i),'_',num2str(k),'.txt');
      A=make_reduce_matrix(A,n,p);
      dlmwrite(name2,A);
        
    end
end
end
end

function A=make_reduce_matrix(A,n,p)
nodes=randsample(size(A,2),n);  %% random nodes to reduce their degree
for i=1:n
    
    d=sum(A(nodes(i),:)); %% degree of each node
    dif = round(d .* (p/100)) ; %% reduce by p%
    if dif >0 
    
    nonzero=find(A(nodes(i),:));
    y = randsample(nonzero,dif); %% randomly chose nodes to diconnect them
    
    
    for j=1:size(y,2)
         
        
         A(i,y(j))=0;
         A(y(j),i)=0;
    end
    end    

end
end