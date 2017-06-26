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
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Diff_betta/' + folders[i] + '/Infected_0.05.txt';
	Y1 =np.loadtxt(text,delimiter='\t') 
	Y1=np.mean(Y1, axis=1)
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Diff_betta/' + folders[i] + '/Infected_0.005.txt';
	Y2 =np.loadtxt(text,delimiter='\t') 
	Y2=np.mean(Y2, axis=1)
	
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Diff_betta/' + folders[i] + '/Infected_0.001.txt';
	Y3 =np.loadtxt(text,delimiter='\t') 
	Y3=np.mean(Y3, axis=1)
	
	text=text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Diff_betta/' + folders[i] + '/Diff_B.pdf';
	data_array=[X,Y1,Y2,Y3];
	legends = [r'$\beta$=0.05',r'$\beta$=0.005',r'$\beta$=0.001']
	plotter.plot(text, data_array, legends, 'Time', 'Cumulative number of infected')


