function Run_Dynamic_Random_Network()

names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};
for j=2:3
    j
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j});
  
  
parfor i=0:100
    i
    %name='/Users/halehashki/Haleh/Thesis/Paper/codes/data/watts_strogatz_Network/Network';
    %%path=strcat(name,'/Networks2/Networks/Network',int2str(i),'.txt')
    path=strcat(name,'/Networks1/Networks/Network',int2str(i),'.txt');
    
    A=dlmread(path);
    %%[N]=SIR_Dynamic_RandomNetwork(path);
    [N]=SIR_SetofNetwork_Dynamic(A);
    
    path2=strcat(name,'/Networks1/Simulation_Dynamic_Netwrok/Result',int2str(i),'.txt');
    dlmwrite(path2,N);

end

end

end