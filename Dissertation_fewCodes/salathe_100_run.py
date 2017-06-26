#!/usr/bin/python
import numpy as np
import csv
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import plotter2

X=range(1,90758)
data_array=[X[0::100]];

for i in range(100):
	text='/Users/halehashki/Haleh/Thesis/Paper/codes/data/salathe/Simulation_Result/N' + str(i+1) + '.txt';
	Y1 =np.loadtxt(text,delimiter=',') 
	Y1=Y1[:,1];
	Y1=Y1[0::100]
	data_array.append(Y1)

#with open("alldata.txt", "wb") as f:
#	writer = csv.writer(f)
#	writer.writerows(data_array)
	
	
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Salathe/100run.pdf';	
plotter2.plot(text, data_array, 'Time', 'Cumulative number of infected')






