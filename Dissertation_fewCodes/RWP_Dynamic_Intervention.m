function RWP_Dynamic_Intervention()
names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};

for j=1:3
    if j==1
        i=5;
    elseif j==2
        i=4;
    elseif j == 3
        i=1;
    end    
   i
       
 %% name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_Intervention/percentage10/result',num2str(i),'.txt');
   %%name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_intervention/percentage10/PercentageResult',num2str(i),'.txt');
   %%name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_intervention/Time30/TimeResult',num2str(i),'.txt');
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/percentage10/Result',num2str(i),'.txt');
   
   %name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/Immunization60/Result',num2str(i),'.txt');
  
  
   N1=dlmread(name); 

  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/percentage20/Result',num2str(i),'.txt');
  N2=dlmread(name); 
  

    name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/percentage30/Result',num2str(i),'.txt');

  N3=dlmread(name); 

  
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/percentage50/Result',num2str(i),'.txt');

  N4=dlmread(name); 
  
  
  name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/percentage70/Result',num2str(i),'.txt');

  N5=dlmread(name); 
 
  path = strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/allresult_nodepercentage.txt');
  Y=[N1(:,1) N2(:,1)  N3(:,1)  N4(:,1)  N5(:,1)];
  dlmwrite(path,Y,'\t');

  
  
  
  
  
  

    
end
end