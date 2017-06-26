#!/usr/bin/python
import numpy as np
import csv
# import matplotlib
# matplotlib.use('PDF')
# import matplotlib.pyplot as plt
import plotter


X=range(1,90752)
# text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Salathe/N_0.0003_0.001_.5.txt';
# Y1 =np.loadtxt(text,delimiter=',') 
# Y1=Y1[1:90752,1]

text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Salathe/N_0.0003_0.001.txt';
Y2 =np.loadtxt(text,delimiter=',') 
Y2=Y2[1:90752,1]

text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Salathe/N_0.0005_0.005.txt';
Y3 =np.loadtxt(text,delimiter=',') 
Y3=Y3[1:90752,1]

text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Salathe/N_0.005_0.05.txt';
Y4 =np.loadtxt(text,delimiter=',') 
Y4=Y4[1:90752,1]


data_array=[X,Y2,Y3,Y4];
##legends = ['B=0.0003, T=.5','B=0.0003, T=.9','B=0.0005, T=.9','B=0.005, T=.9']
##legends = [r'$\beta=0.0003, \tau=.5$',r'$\beta=0.0003, \tau=.9$',r'$\beta=0.0005, \tau=.9$',r'$\beta=0.005, \tau=.9$']
legends = [r'$\beta=0.0003$',r'$\beta=0.0005$',r'$\beta=0.005$']
text='/Users/halehashki/Haleh/Thesis/Paper/codes/plots/Salathe/Diff_parameter.pdf';
plotter.plot(text, data_array, legends, 'Time', 'Cumulative number of infected')









