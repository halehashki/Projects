function Dynamic_meandegree()


for i=790: 2355   %%i=195:2355    %%% 2160 steps equal to 12 hours
    i
       %% if i ~= 789
filepath='/Users/halehashki/Haleh/Thesis/Research/salathe/moteFiles/TimeStamp/';
nodeid=strcat('Time',int2str(i));
filename=strcat(filepath,nodeid);
fid = fopen(filename);
fileind=fgets(fid);
        
if fileind ~= -1
     % A=zeros(n,n);
    
    


T= dlmread(filename);



R1=T(1,:);
R2=T(2,:);
for j=1:size(R1,2)
A(R1(j),R2(j))=1;
end


    S=sum(A);
    u=unique(S);
    count=histc(S,unique(S));
    p=count/size(R1,2);
    k=u*p';
    u2=u-1;
    u3=u2.*u;
    k2=u3*p';
    
    t=[k,k2];
    
    
    s=svd(A);
    
    
    path1='/Users/halehashki/Haleh/Thesis/Paper/codes/data/salathe/R0_result/Degree/meandegree';
filename1=strcat(path1,int2str(i),'.txt');

dlmwrite(filename1, t);

 path2='/Users/halehashki/Haleh/Thesis/Paper/codes/data/salathe/R0_result/SVD/eigenvalue';
filename2=strcat(path2,int2str(i),'.txt');

dlmwrite(filename2, s);
end
      %%  end
        fclose(fid);
end
    
end