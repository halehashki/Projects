#!/usr/bin/env python
import os
import math
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt


#from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
### for Palatino and other serif fonts use:
##rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)
# this sets the default fontsize for the plots
from matplotlib import rcParams
rcParams['axes.labelsize'] = 20
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
rcParams['legend.fontsize'] = 20


# this reads from one file 4 columns for example
# time susceptibles infected recovered
# or
# time barabasidata erdoesdata wattsdata
#
# running the program from the commandline delibers an example plot
# importing it as plotter
# and then call the function
#
# import plotter
# plotter.plot(outfilename, data_array, legends, xlabel, ylabel)
#        outfilename: is the filename the plot is saved to
#        data_array: should be of the form [allx,ally1, ally2, ...]
#        legends: an array of texts to fit the ally1, ally2,...]
#        xlabel: label for the X axis
#        ylabel: label for the Y axis
#
def plot(outfilename, data_array, legends, xtitle, ytitle):
    fig, ax = plt.subplots()
    x = data_array[0]
    y = data_array[1:]
    columns = len(data_array)
    # lines with symbols
    #symbols = ['-k*',':ko','--k','-ko','--k*','--ko']
    # only lines
    symbols = ['-k',':k','--k','-ko','--k','--k']
    while columns > len(symbols):
        symbols.extend(symbols)
    symbols = symbols[:columns]
    graphx = range(columns) #init of the graphs
    for yi,gi,si,li in zip(y,graphx,symbols,legends):
    	gi, = ax.plot(x,yi,si,mfc='white', label=li)
    	gi.set_markevery(20)
    handles, labels = ax.get_legend_handles_labels()
    lll = plt.legend(handles, legends,handletextpad=0.01, ncol=2, loc=4)
    lll.get_frame().set_linewidth(0)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.ylim((0,1000))
    plt.tight_layout()
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    #ax.set_ylim(5,500)
    #ax.set_yticks([5,10,50,100,500])
    #ax.set_yticklabels(['5','10','50','100','500'])
    #ax.set_xlim(0.005,0.8)
    #ax.set_xticks([0.005,0.01,0.05,0.1,0.5])
    #ax.set_xticklabels(['0.005','0.01','0.05', '0.1','0.5'])
    plt.savefig(outfilename, format='pdf')



if __name__ == '__main__':
    import random
    from math import *
    x = sorted([random.uniform(0.0,5.0) for xi in range(100)])
    y1 = [sin(xi) for xi in x ]
    y2 = [sin(xi * xi) for xi in x ]
    y3 = [sin(xi) * exp(-xi) for xi in x ]
    data = [x, y1, y2, y3]
    legends = [r'$\sin(x)$',r'$\sin(x^2)$',r'$\sin(x)*e^{-x}$']
    plot("testplot.pdf",data,legends,r'Time $\xi$',r'Mutation rate $\mu$')
