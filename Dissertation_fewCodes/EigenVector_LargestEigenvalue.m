function EigenVector_LargestEigenvalue()
names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};
networks={'9','40','70','90'};
for j=3:3
    for i=1:4
        
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Networks/Network', networks{i},'.txt');

A=dlmread(name);
%%% laplacian is not working correctly
% L=diag(sum(A))-A;
% [V E]=eig(L);
% [ES EI]=sort(diag(E),'descend');
% EH=V(:,EI(1));
% [va nodes]=sort(EH,'descend');  %% values and index of the sortes eigenvector of the largest eigenvale

[V E]=eig(A);
[va nodes]=sort(V(:,size(A,1)),'descend');

[N]=SIR_Static_Intervention(A,1000,nodes(1:1),1001)
[N1]=SIR_Static_Intervention(A,1000,nodes(1:300),30)
[N2]=SIR_Static_Intervention(A,1000,nodes(1:300),150)
[N3]=SIR_Static_Intervention(A,1000,nodes(1:300),250)
[N4]=SIR_Static_Intervention(A,1000,nodes(1:300),350)


path=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Intervention_30percentage_time_larger',networks{i},'.jpg');
f=figure(2)
plot(N(:,1),'--b')
hold on
plot(N1(:,1),'-r')
hold on
plot(N2(:,1),'-g')
hold on
plot(N3(:,1),'-b')
hold on
plot(N4(:,1),'-m')


legend('No Intervention','At time 30','At time 150','At time 250','At time 300');
xlabel('Time step')
ylabel('Cumulative Infected')
saveas(f,path)
close(f)

    end
end
end