#!/usr/bin/python
import numpy as np
import csv
# import matplotlib
# matplotlib.use('PDF')
# import matplotlib.pyplot as plt
import plotter_dynamic 

# folders=['barabasi','erdos','watts'];
# for i in range(3):
X=range(1,1001)
text='/Users/halehashki/Haleh/Thesis/Paper/codes/data/barabasi_albert_Network/Networks2/Simulation_Result/Result4.txt';
H =np.loadtxt(text,delimiter='\t')
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/barabasi/Dynamic_intervention/Time_allresult.txt';
Y =np.loadtxt(text,delimiter='\t') 
Y0=H[:,0];
Y1=Y[:,0];
Y2=Y[:,1];
Y3=Y[:,2];
data_array=[X,Y0,Y1,Y2,Y3];
legends = [r'None','30','50','100']
#legends = [r'$0\%$',r'$10\%$',r'$20\%$',r'$30\%$']
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/barabasi/Dynamic_intervention/Intervention_time.pdf';
plotter_dynamic.plot(text, data_array, legends, 'Time', 'Cumulative Number of Infected')

	
	
	
X=range(1,1001)
text='/Users/halehashki/Haleh/Thesis/Paper/codes/data/erdos_renyi_Network/Networks2/Simulation_Result/Result76.txt';
H =np.loadtxt(text,delimiter='\t')
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/erdos/Dynamic_intervention/Time_allresult.txt';
Y =np.loadtxt(text,delimiter='\t') 
Y0=H[:,0];
Y1=Y[:,0];
Y2=Y[:,1];
Y3=Y[:,2];
data_array=[X,Y0,Y1,Y2,Y3];
legends = [r'None','30','50','100']
#legends = [r'$0\%$',r'$10\%$',r'$20\%$',r'$30\%$']
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/erdos/Dynamic_intervention/Intervention_time.pdf';
plotter_dynamic.plot(text, data_array, legends, 'Time', 'Cumulative Number of Infected')



	
X=range(1,1001)
text='/Users/halehashki/Haleh/Thesis/Paper/codes/data/watts_strogatz_Network/Networks2/Simulation_Result/Result1.txt';
H =np.loadtxt(text,delimiter='\t')
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/watts/Dynamic_intervention/Time_allresult.txt';
Y =np.loadtxt(text,delimiter='\t') 
Y0=H[:,0];
Y1=Y[:,0];
Y2=Y[:,1];
Y3=Y[:,2];
data_array=[X,Y0,Y1,Y2,Y3];
legends = [r'None','30','50','100']
#legends = [r'$0\%$',r'$10\%$',r'$20\%$',r'$30\%$']
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Intervention_Node/watts/Dynamic_intervention/Intervention_time.pdf';
plotter_dynamic.plot(text, data_array, legends, 'Time', 'Cumulative Number of Infected')

		
	
	
	
	
	
	
	
	