#!/usr/bin/python
import numpy as np
import csv
# import matplotlib
# matplotlib.use('PDF')
# import matplotlib.pyplot as plt
import plotter


folders=['barabasi','erdos','watts'];
for i in range(3):
	X=range(1,1001)
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_9.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	#legends = ['No Intervention','Time 30','Time 50','Time 100','Time 130']
	legends = ['None','30','50','100','130']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_9.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative Number of Infected')
	
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_40.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	legends = ['None','30','50','100','130']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_40.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative number of infected')
	
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_70.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	legends = ['None','30','50','100','130']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_70.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative number of infected')
	
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_90.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	legends = ['None','30','50','100','130']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Time/' + folders[i] + '/Intervention_30percentage_diffTime_new_90.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative number of infected')
	
	
	
	
	
	
	
	