function RWP_EigenVector_LargestEigenvalue()
names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};
names2={'barabasi';'erdos';'watts'};
networks={'9','40','70','90'};

for j=1:3
    j
    for i=1:4
     i   
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Networks/Network', networks{i},'.txt');

A=dlmread(name);
L=diag(sum(A))-A;
[V E]=eig(L);
[ES EI]=sort(diag(E),'descend');
EH=V(:,EI(1));
[va nodes]=sort(EH,'descend');  %% values and index of the sortes eigenvector of the largest eigenvale


[N]=SIR_Static_Intervention(A,1000,nodes(1:1),1001);
[N1]=SIR_Static_Intervention(A,1000,nodes(1:300),30);
[N2]=SIR_Static_Intervention(A,1000,nodes(1:300),50);
[N3]=SIR_Static_Intervention(A,1000,nodes(1:300),100);
[N4]=SIR_Static_Intervention(A,1000,nodes(1:300),1300);


path=strcat('//Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/',names2{j},'/Intervention_30percentage_diffTime_new_',networks{i},'.txt');
Y=[N(:,1)  N1(:,1)  N2(:,1)  N3(:,1) N4(:,1)];
dlmwrite(path,Y,'\t');


    end
end
end