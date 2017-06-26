#!/usr/bin/env python
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import plotter
import plotter3
import numpy as np
CalifoniaPopMonthly=np.loadtxt('./PopulationMonthly.txt', delimiter=',')
#print "----- ", len(CalifoniaPopMonthly1), len(CalifoniaPopMonthly)

Samplepop=np.loadtxt('./SamplePopulation.txt', delimiter=',')
#Samplepop=np.loadtxt('./SamplePopulation.txt', delimiter=',')
popave=np.average(Samplepop)


RFDiabetes=np.loadtxt('./All_RF_Diabetes.txt', dtype=None)
FB_RFDiabetes=np.loadtxt('./All_FB_RFDiabetes.txt', dtype=None)
USB_RFDiabetes=np.loadtxt('./All_USB_RFDiabetes.txt', dtype=None)
#RFDiabetes=np.loadtxt('./Avg_Diabetes_val.txt')
RFSmokers=np.loadtxt('./All_RFSmokers.txt',  dtype=None)
FB_RFSmokers=np.loadtxt('./All_FB_RFSmokers.txt',  dtype=None)
USB_RFSmokers=np.loadtxt('./All_USB_RFSmokers.txt',  dtype=None)


#RFSmokers=np.loadtxt('./Avg_Smoking_val.txt')
RFESRD=np.loadtxt('./All_RF_ESRD.txt',  dtype=None)
FB_RFESRD=np.loadtxt('./All_FB_RFESRD.txt',  dtype=None)
USB_RFESRD=np.loadtxt('./All_USB_RFESRD.txt',  dtype=None)
#RFESRD=np.loadtxt('./Avg_ESRD_val.txt')

RFHIV=np.loadtxt('./All_RF_HIV.txt', dtype=None)
FB_RFHIV=np.loadtxt('./All_FB_RFHIV.txt', dtype=None)
USB_RFHIV=np.loadtxt('./All_USB_RFHIV.txt', dtype=None)
#RFHIV=np.loadtxt('./Avg_HIV_val.txt')

#Death=np.loadtxt('../Results/Deadrate.txt',  delimiter=',')

X=range(0,144)

####### Scaling up

#aa= np.multiply(RFDiabetes, CalifoniaPopMonthly[3:len(CalifoniaPopMonthly)])



#aa= np.multiply(RFSmokers, CalifoniaPopMonthly[3:len(CalifoniaPopMonthly)])
aa= np.multiply(RFSmokers, CalifoniaPopMonthly[0:len(RFSmokers)])
RFSmokers=np.divide(aa,Samplepop[0:len(Samplepop)])

aa= np.multiply(FB_RFSmokers, CalifoniaPopMonthly[0:len(FB_RFSmokers)])
FB_RFSmokers=np.divide(aa,Samplepop[0:len(Samplepop)])

aa= np.multiply(USB_RFSmokers, CalifoniaPopMonthly[0:len(USB_RFSmokers)])
USB_RFSmokers=np.divide(aa,Samplepop[0:len(Samplepop)])




aa= np.multiply(FB_RFDiabetes, CalifoniaPopMonthly[0:len(FB_RFDiabetes)])
FB_RFDiabetes=np.divide(aa,Samplepop[0:len(Samplepop)])


aa= np.multiply(USB_RFDiabetes, CalifoniaPopMonthly[0:len(USB_RFDiabetes)])
USB_RFDiabetes=np.divide(aa,Samplepop[0:len(Samplepop)])


aa= np.multiply(RFDiabetes, CalifoniaPopMonthly[0:len(RFDiabetes)])
RFDiabetes=np.divide(aa,Samplepop[0:len(Samplepop)])


#aa= np.multiply(RFESRD, CalifoniaPopMonthly[3:len(CalifoniaPopMonthly)])
aa= np.multiply(RFESRD, CalifoniaPopMonthly[0:len(RFESRD)])
RFESRD=np.divide(aa,Samplepop[0:len(Samplepop)])

aa= np.multiply(FB_RFESRD, CalifoniaPopMonthly[0:len(FB_RFESRD)])
FB_RFESRD=np.divide(aa,Samplepop[0:len(Samplepop)])


aa= np.multiply(USB_RFESRD, CalifoniaPopMonthly[0:len(USB_RFESRD)])
USB_RFESRD=np.divide(aa,Samplepop[0:len(Samplepop)])




#aa= np.multiply(RFHIV, CalifoniaPopMonthly[3:len(CalifoniaPopMonthly)])
aa= np.multiply(RFHIV, CalifoniaPopMonthly[0:len(RFHIV)])
RFHIV=np.divide(aa,Samplepop[0:len(Samplepop)])

aa= np.multiply(FB_RFHIV, CalifoniaPopMonthly[0:len(FB_RFHIV)])
FB_RFHIV=np.divide(aa,Samplepop[0:len(Samplepop)])

aa= np.multiply(USB_RFHIV, CalifoniaPopMonthly[0:len(USB_RFHIV)])
USB_RFHIV=np.divide(aa,Samplepop[0:len(Samplepop)])




X=range(0,144)

data_array=[X,RFDiabetes[0:144]]
legends = ['Diabetes']
text='./Figures/RFDiabetes.pdf'
plotter.plot(text, data_array, legends, 'Months', 'Population')

data_array=[X,RFSmokers[0:144]]
legends = ['Smokers']
text='./Figures/RFSmokers.pdf'
plotter.plot(text, data_array, legends, 'Months', 'Population')


data_array=[X,RFESRD[0:144]]
legends = ['ESRD']
text='./Figures/RFESRD.pdf'
plotter.plot(text, data_array, legends, 'Months', 'Population')


data_array=[X,RFHIV[0:144]]
legends = ['HIV']
text='./Figures/RFHIV.pdf'
plotter.plot(text, data_array, legends, 'Months', 'Population')

###### Yearly
RFDiabetesYearly=[]
for i in range(0,len(RFDiabetes),12):
    # aa=RFDiabetes[i:i+11]
    # RFDiabetesYearly.append(sum(aa))
    aa=RFDiabetes[i]
    RFDiabetesYearly.append(aa)

FB_RFDiabetesYearly=[]
for i in range(0,len(FB_RFDiabetes),12):
    # aa=RFDiabetes[i:i+11]
    # RFDiabetesYearly.append(sum(aa))
    aa=FB_RFDiabetes[i]
    FB_RFDiabetesYearly.append(aa)


USB_RFDiabetesYearly=[]
for i in range(0,len(USB_RFDiabetes),12):
    # aa=RFDiabetes[i:i+11]
    # RFDiabetesYearly.append(sum(aa))
    aa=USB_RFDiabetes[i]
    USB_RFDiabetesYearly.append(aa)



RFSmokersYearly=[]
for i in range(0,len(RFSmokers),12):
    # aa=RFSmokers[i:i+11]
    # RFSmokersYearly.append(sum(aa))
    aa=RFSmokers[i]
    RFSmokersYearly.append(aa)


FB_RFSmokersYearly=[]
for i in range(0,len(FB_RFSmokers),12):
    # aa=RFSmokers[i:i+11]
    # RFSmokersYearly.append(sum(aa))
    aa=FB_RFSmokers[i]
    FB_RFSmokersYearly.append(aa)

USB_RFSmokersYearly=[]
for i in range(0,len(USB_RFSmokers),12):
    # aa=RFSmokers[i:i+11]
    # RFSmokersYearly.append(sum(aa))
    aa=USB_RFSmokers[i]
    USB_RFSmokersYearly.append(aa)







RFESRDYearly=[]
for i in range(0,len(RFESRD),12):
    # aa=RFESRD[i:i+11]
    # RFESRDYearly.append(sum(aa))
    aa=RFESRD[i]
    RFESRDYearly.append(aa)


FB_RFESRDYearly=[]
for i in range(0,len(FB_RFESRD),12):
    # aa=RFESRD[i:i+11]
    # RFESRDYearly.append(sum(aa))
    aa=FB_RFESRD[i]
    FB_RFESRDYearly.append(aa)

USB_RFESRDYearly=[]
for i in range(0,len(USB_RFESRD),12):
    # aa=RFESRD[i:i+11]
    # RFESRDYearly.append(sum(aa))
    aa=USB_RFESRD[i]
    USB_RFESRDYearly.append(aa)




RFHIVYearly=[]
for i in range(0,len(RFHIV),12):
    # aa=RFHIV[i:i+11]
    # RFHIVYearly.append(sum(aa))
    aa=RFHIV[i]
    RFHIVYearly.append(aa)


FB_RFHIVYearly=[]
for i in range(0,len(FB_RFHIV),12):
    # aa=RFHIV[i:i+11]
    # RFHIVYearly.append(sum(aa))
    aa=FB_RFHIV[i]
    FB_RFHIVYearly.append(aa)



USB_RFHIVYearly=[]
for i in range(0,len(USB_RFHIV),12):
    # aa=RFHIV[i:i+11]
    # RFHIVYearly.append(sum(aa))
    aa=USB_RFHIV[i]
    USB_RFHIVYearly.append(aa)



np.savetxt('RFHIVYearly.txt', RFHIVYearly,fmt='%1.3f', delimiter=',')
np.savetxt('FB_RFHIVYearly.txt', FB_RFHIVYearly,fmt='%1.3f', delimiter=',')
np.savetxt('USB_RFHIVYearly.txt', USB_RFHIVYearly,fmt='%1.3f', delimiter=',')
np.savetxt('RFESRDYearly.txt', RFESRDYearly,fmt='%1.3f', delimiter=',')
np.savetxt('FB_RFESRDYearly.txt', FB_RFESRDYearly,fmt='%1.3f', delimiter=',')
np.savetxt('USB_RFESRDYearly.txt', USB_RFESRDYearly,fmt='%1.3f', delimiter=',')
np.savetxt('RFSmokersYearly.txt', RFSmokersYearly,fmt='%1.3f', delimiter=',')
np.savetxt('FB_RFSmokersYearly.txt', FB_RFSmokersYearly,fmt='%1.3f', delimiter=',')
np.savetxt('USB_RFSmokersYearly.txt', USB_RFSmokersYearly,fmt='%1.3f', delimiter=',')
np.savetxt('RFDiabetesYearly.txt', RFDiabetesYearly,fmt='%1.3f', delimiter=',')
np.savetxt('FB_RFDiabetesYearly.txt', FB_RFDiabetesYearly,fmt='%1.3f', delimiter=',')
np.savetxt('USB_RFDiabetesYearly.txt', USB_RFDiabetesYearly,fmt='%1.3f', delimiter=',')
############ CDPH data 2001
# Control_Diabetes=[1618772 ,1890080,1875353,1849994,1886718,2198866,2071612,2367595,2550223,2423314,2219754,2824278,2969755]
# Contro_ESRD=[47809,50784,53382,55840,57954,60395,63330,66302,69748,73548,76632,80152,0]
# Contro_Smoking=[4187723.6,4169460.74,4127230.95,3946140.56,3817929.92,3798338.89,3974503.22,3864185.86,3816391.04,3534471.48,3607805.16,3862780.44,3595802.3]
# Contro_HIV=[0,0,0,0,0,0,0,171200,173800,176800,179900,183300,0]


Control_Diabetes=[1875353,1849994,1886718,2198866,2071612,2367595,2550223,2423314,2219754,2824278,2969755]
#Contro_ESRD=[53382,55840,57954,60395,63330,66302,69748,73548,76632,80152,0]
Contro_ESRD=[53382,55840,57954,60395,63330,66302,69748,73548,76632,80152]
Contro_Smoking=[4127230.95,3946140.56,3817929.92,3798338.89,3974503.22,3864185.86,3816391.04,3534471.48,3607805.16,3862780.44,3595802.3]
Contro_HIV=[0,0,0,0,0,171200,173800,176800,179900,183300,0]

##########Plot for Yearly
#X=range(13)
X=range(2003,2014)
print len(RFESRDYearly[0:len(Contro_ESRD)]), len(Contro_ESRD)
print len(RFDiabetesYearly), len(Control_Diabetes)
print len(RFSmokersYearly), len(Contro_Smoking)
print len(RFHIVYearly), len(Contro_HIV)

data_array=[X,RFDiabetesYearly[0:len(Control_Diabetes)],Control_Diabetes]
legends = ['Average of model runs','Calif. reported Diabetes cases']
text='./Figures/RFDiabetesYearly.pdf'
plotter.plot(text, data_array, legends, 'Years', 'Diabetes Population')

data_array=[X,RFSmokersYearly[0:len(Contro_Smoking)],Contro_Smoking]
legends = ['Average of model runs','Calif. reported Smoking cases']
text='./Figures/RFSmokersYearly.pdf'
plotter.plot(text, data_array, legends, 'Years', 'Smoking Population')

X=range(2003,2013)
data_array=[X,RFESRDYearly[0:len(Contro_ESRD)],Contro_ESRD]
legends = ['Average of model runs','Calif. reported ESRD cases']
text='./Figures/RFESRDYearly.pdf'
plotter.plot(text, data_array, legends, 'Years', 'ESRD Population')

Contro_HIV=[171200,173800,176800,179900,183300]
X1=range(2003,2014)
X2=range(2008,2013)
data_arrayx=[X1,X2]
data_arrayy=[RFHIVYearly[0:len(X1)],Contro_HIV]
legends = ['Average of model runs','Calif. reported HIV cases']
text='./Figures/RFHIVYearly.pdf'
plotter3.plot(text, data_arrayx, data_arrayy, legends, 'Years', 'HIV Population')
