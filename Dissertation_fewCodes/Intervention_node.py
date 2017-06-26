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
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_9.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	#legends = ['No Intervention','10%','20%','30%','40%']
	legends = [r'0\%','10\%','20\%','30\%','40\%']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_9.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative Number of Infected')
	
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_40.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	legends = [r'0\%','10\%','20\%','30\%','40\%']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_40.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative Number of Infected')
	
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_70.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	legends = [r'0\%','10\%','20\%','30\%','40\%']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_70.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative number of infected')
	
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_90.txt';
	Y =np.loadtxt(text,delimiter='\t') 
	Y1=Y[:,0];
	Y2=Y[:,1];
	Y3=Y[:,2];
	Y4=Y[:,3];
	Y5=Y[:,4];
	data_array=[X,Y1,Y2,Y3,Y4,Y5];
	legends = [r'0\%','10\%','20\%','30\%','40\%']
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/' + folders[i] + '/Intervention_percentage_90.pdf';
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative number of infected')

	
	
	
	
	
	
	