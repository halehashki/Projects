#!/usr/bin/env python
import os
import math
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt


# this sets the default fontsize for the plots
from matplotlib import rcParams
rcParams['axes.labelsize'] = 10
rcParams['xtick.labelsize'] = 10
rcParams['ytick.labelsize'] = 10
rcParams['legend.fontsize'] = 10


def plot(outfilename, data_array, legends, xtitle, ytitle):
    fig, ax = plt.subplots()
    x = data_array[0]
    y = data_array[1:]
    columns = len(data_array)
    # lines with symbols
    symbols = ['-k*',':ko','--k','-ko','--k*','--ko']
    # only lines
    #symbols = ['-k',':k','--k','-ko','--k*','--ko']
    symbols = ['b','g','r','c','m','y','k']
    #symbols = ['b*','bo','-g*','-go',':go','-r*','-ro',':ro']
    while columns > len(symbols):
        symbols.extend(symbols)
    symbols = symbols[:columns]
    graphx = range(columns) #init of the graphs
    for yi,gi,si,li in zip(y,graphx,symbols,legends):
        gi, = ax.plot(x,yi,si,mfc='white', label=li,linewidth=4)
        #gi.set_markevery(20)
    handles, labels = ax.get_legend_handles_labels()
    lll = plt.legend(handles, legends,handletextpad=0.01, loc=1,prop={'size':10})
    lll.get_frame().set_linewidth(0)
    ax.set_ylim(ymin=0)
    plt.xlabel(xtitle,fontsize=16)
    plt.ylabel(ytitle,fontsize=16)
    plt.tight_layout()
    plt.savefig(outfilename, format='pdf')
