#!/usr/bin/python
import numpy as np
import csv
import os
import math
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt

# import plotter_area
# import plotter2



X=range(1,1001)
B =np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/barabasi_I.txt',delimiter='\t') 
Bup =np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/barabasi_I_areaUP.txt',delimiter='\t') 
Bdown =np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/barabasi_I_areaDown.txt',delimiter='\t') 


E= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/Erdos_I.txt',delimiter='\t') 
Eup= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/Erdos_I_areaUP.txt',delimiter='\t') 
Edown= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/Erdos_I_areaDown.txt',delimiter='\t') 


W= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/watts_I.txt',delimiter='\t') 
Wup= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/watts_I_areaUP.txt',delimiter='\t') 
Wdown= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/watts_I_areaDown.txt',delimiter='\t') 

from matplotlib import rcParams
rcParams['axes.labelsize'] = 20
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
rcParams['legend.fontsize'] = 20


plt.plot(X,B, '-k')
plt.fill_between(X, Bup, Bdown, alpha=0.3,  facecolor='#808080')

plt.plot(X,E, ':k')
plt.fill_between(X, Eup, Edown, alpha=0.3,  facecolor='#808080',)

plt.plot(X,W, '--k')
plt.fill_between(X, Wup, Wdown, alpha=0.3,  facecolor='#808080',)

legends = [r'Bar\'abasi-Albert',r'Erd\H{o}s-R\'{e}nyi',r'Watts-Strogatz']
plt.rc('text',usetex=True)
lll = plt.legend(legends,handletextpad=0.01, loc=4)
lll.get_frame().set_linewidth(0)
plt.xlabel('Time')
plt.ylabel('Cumulative number of infected')
plt.ylim((0,1000))
#plt.show()
plt.tight_layout()

plt.savefig('all_nework_n1000_k10_I_area.pdf', format='pdf')


# data_array=[X,B,Bup,Bdown,E,Eup,Edown,W,Wup,Wdown];
# legends = [r'Barabasi-Albert',r'Erd\H{o}s-R\'{e}nyi',r'Watts-Strogatz']
# plotter_area.plot('all_nework_n1000_k10.pdf', data_array, legends, 'Time', 'Cumulative number of infected')




# B =np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/barabasi_I_R.txt',delimiter='\t') 
# E= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/Erdos_I_R.txt',delimiter='\t') 
# W= np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/plots/All_Networks/watts_I_R.txt',delimiter='\t') 
# 
# 
# data_array=[X,B,E,W];
# legends = [r'Barabasi-Albert',r'Erd\H{o}s-R\'{e}nyi',r'Watts-Strogatz']
# plotter2.plot('all_nework_n1000_k10_I_R.pdf', data_array, legends, 'Time', 'Number of infected')
