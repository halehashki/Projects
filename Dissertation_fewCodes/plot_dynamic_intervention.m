function plot_dynamic_intervention()

names={'barabasi_albert_Network';'erdos_renyi_Network';'watts_strogatz_Network'};

%%%% plotting dynamic_network_intervention

int_time=[30,50,100];
int_per=[10,20,30];

for i=1:5 %%% 5 random netwroks
    i
    for j=1:3  %%% BA,ER,WS 
        j
        for k=1:3  
       k   
     
        
    
    %path=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_Intervention/','Time',num2str(int_time(k)),'/Result',num2str(i),'.txt');
    %path=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_Intervention/','percentage',num2str(int_per(k)),'/Result',num2str(i),'.txt');
    
    path=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_intervention/','percentage',num2str(int_per(k)),'/PercentageResult',num2str(i),'.txt');
    N=dlmread(path);
    
     
 
    f=figure(1);  

    plot(N(:,1))
    hold on


    
        end
       p=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_intervention/Intervention_Result_percentage',num2str(i),'.jpg');
       %p=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_Intervention/Intervention_Result_percentage',num2str(i),'.jpg');
     % p=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_Intervention/Intervention_Result_Time',num2str(i),'.jpg');
      %legend('Barabasi-Albert','Erdos-Renyi','Watts-Strogatz');
       
        xlabel('Time step')
        ylabel('Infected')
        saveas(f,p);
     close(f)
     
    end
end
     



for i=1:5 %%% 5 random netwroks
    i
    for j=1:3  %%% BA,ER,WS 
        j
        for k=1:3  
       k   
     
     path=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_intervention/','Time',num2str(int_time(k)),'/TimeResult',num2str(i),'.txt');
    N=dlmread(path);
    
     
 
    f=figure(1);  

    plot(N(:,1))
    hold on


    
        end
      p=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_intervention/Intervention_Result_time',num2str(i),'.jpg');
      % p=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_Intervention/Intervention_Result_percentage',num2str(i),'.jpg');
     % p=strcat('/Users/halehashki/Haleh/Thesis/Paper/codes/data/',names{j},'/Networks2/Intervention/Dynamic_Network_Intervention/Intervention_Result_Time',num2str(i),'.jpg');
      %legend('Barabasi-Albert','Erdos-Renyi','Watts-Strogatz');
       
        xlabel('Time step')
        ylabel('Infected')
        saveas(f,p);
     close(f)
     
     
     
     
     
     
    end
end





end