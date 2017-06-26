function make_dynamic_intervention_pagerank()

names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};
% 
% immunization=[60,80,90];
% int_per=[50,70];
% for j=1:3
%     j
%     for k=1:3
%         k
%      for i=1:5
%      i   
%     name=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Networks/Network', num2str(i),'.txt');
%     A=dlmread(name);
%     
%     
% 
%      % [N]=SetofNetwork_Dynamic_Intervention_PageRank(A,50,int_per(k));
%       [N]=SetofNetwork_Dynamic_Intervention_PageRank(A,50,30,immunization(k)/100);
%     
%     
%    
%     path=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank','/Immunization',num2str(immunization(k)),'/Result',num2str(i),'.txt');
%     dlmwrite(path,N);
%      end
%     end
% end


%%% plot the result

immunization=[60,80,90];
int_per=[10,20,30,50,70];
for i=1:5 %%% 5 random netwroks
    i
    for j=1:3  %%% BA,ER,WS 
        j
        for k=1:3  
       k   
     
        
    
  
    path=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank','/Immunization',num2str(immunization(k)),'/Result',num2str(i),'.txt');
    N=dlmread(path);
    
     
 
    f=figure(1);  

    plot(N(:,1))
    hold on


    
        end
       p=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_PageRank/Intervention_pagerank_immunization_',num2str(i),'.jpg');
       
       
        xlabel('Time step')
        ylabel('Infected')
        saveas(f,p);
     close(f)
     
    end
end




end