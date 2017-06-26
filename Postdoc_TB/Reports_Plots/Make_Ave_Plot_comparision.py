#!/usr/bin/env python
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import plotter
import plotter3
import numpy as np
import pandas as pd
import collections

Control_TB_D=[0,0,0,0,0,0,0,425,477,445,474,459]
Control_TB_E=[0,0,0,0,0,0,0,82,87,84,74,82]
Control_TB_H=[185,139,148,153,141,136,109,101,101,88,76,86]
RCVT=np.loadtxt('./RCVT.txt') #,  delimiter=',')
meanval=[]
stdval=[]

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_RFDiabetes.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_RFDiabetes_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_RFDiabetes_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_RFDiabetes_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_RFDiabetes.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_RFDiabetes.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_RFDiabetes_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_RFDiabetes_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_RFDiabetes_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_RFDiabetes.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_RFSmokers.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_RFSmokers_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_RFSmokers_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_RFSmokers_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_RFSmokers.txt',y , delimiter=',')



##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_RFSmokers.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_RFSmokers_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_RFSmokers_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_RFSmokers_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_RFSmokers.txt',y , delimiter=',')




##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_RFSmokers.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_RFSmokers_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_RFSmokers_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_RFSmokers_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_RFSmokers.txt',y , delimiter=',')

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_RFHIV.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_RFHIV_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_RFHIV_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_RFHIV_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_RFHIV.txt',y , delimiter=',')

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_TB_HIV.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_TB_HIV_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_TB_HIV_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_TB_HIV_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_TB_HIV.txt',y , delimiter=',')

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_TB_HIV.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_TB_HIV_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_TB_HIV_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_TB_HIV_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_TB_HIV.txt',y , delimiter=',')

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_TB_Diabetes.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_TB_Diabetes_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_TB_Diabetes_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_TB_Diabetes_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_TB_Diabetes.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_TB_Diabetes.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_TB_Diabetes_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_TB_Diabetes_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_TB_Diabetes_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_TB_Diabetes.txt',y , delimiter=',')










##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_RFESRD.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_RFESRD_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_RFESRD_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_RFESRD_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_All_FB_RFESRD.txt',y , delimiter=',')

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_RFESRD.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_RFESRD_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_RFESRD_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_RFESRD_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_RFESRD.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_RFHIV.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_RFHIV_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_RFHIV_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_RFHIV_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_RFHIV.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_TB_HIV.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_TB_HIV_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_TB_HIV_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_TB_HIV_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_TB_HIV.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_TB_Diabetes.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_TB_Diabetes_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_TB_Diabetes_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_TB_Diabetes_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_TB_Diabetes.txt',y , delimiter=',')

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_TB_Diabetes.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_TB_Diabetes_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_TB_Diabetes_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_TB_Diabetes_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_TB_Diabetes.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_TB_ESRD.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_TB_ESRD_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_TB_ESRD_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_TB_ESRD_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_TB_ESRD.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_TB_ESRD.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_TB_ESRD_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_TB_ESRD_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_TB_ESRD_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_TB_ESRD.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_TB_Smoking.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_TB_Smoking_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_TB_Smoking_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_TB_Smoking_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_TB_Smoking.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_TB_Smoking.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_TB_Smoking_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_TB_Smoking_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_TB_Smoking_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_TB_Smoking.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_TB_Smoking.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_TB_Smoking_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_TB_Smoking_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_TB_Smoking_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_TB_Smoking.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_Fast_latent.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_Fast_latent_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_Fast_latent_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_Fast_latent_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_Fast_latent.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_Slow_latent.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_Slow_latent_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_Slow_latent_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_Slow_latent_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_Slow_latent.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_Fast_latent.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_Fast_latent_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_Fast_latent_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_Fast_latent_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_All_FB_Fast_latent.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_slow_latent.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_FB_slow_latent_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_slow_latent_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_slow_latent_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_slow_latent.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_Population.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_Population_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_Population_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_Population_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_Population.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_FB_Population.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])

    Active_all.append(ActiveYearly)

np.savetxt('All_FB_Population_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_FB_Population_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_FB_Population_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_FB_Population.txt',y , delimiter=',')



##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_USB_Population.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        #aa=TB_active[i:i+11]
        #ActiveYearly.append(sum(aa))
        ActiveYearly.append(TB_active[i])
    Active_all.append(ActiveYearly)

np.savetxt('All_USB_Population_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_USB_Population_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_USB_Population_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_USB_Population.txt',y , delimiter=',')



##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_Tested.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_Tested_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_Tested_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_Tested_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_Tested.txt',y , delimiter=',')

##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_HCW_Tested.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_HCW_Tested_Yearly.txt' ,Active_all, delimiter=',')

Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_HCW_Tested_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_HCW_Tested_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_HCW_Tested.txt',y , delimiter=',')


##############
meanval=[]
stdval=[]

RR=np.loadtxt('./All_Activecases.txt', dtype=None)

Active_all=[]
for i in range(len(RR)):
    ActiveYearly=[]
    TB_active=RR[i]
    for i in range(0,len(TB_active),12):
        aa=TB_active[i:i+11]
        ActiveYearly.append(sum(aa))
    Active_all.append(ActiveYearly)

np.savetxt('All_Activecases_Yearly.txt' ,Active_all, delimiter=',')
print "-----------", Active_all
Rows=range(len(Active_all))

Columns=range(len(ActiveYearly))
dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
filename= './All_Activecases_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./All_Activecases_all.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


y = np.array(meanval)
e = np.array(stdval)

np.savetxt('./Ave_Activecases.txt',y , delimiter=',')




#
#
#
#
#
# #################
# RR=np.loadtxt('./All_Activecases.txt', dtype=None)
#
# Active_all=[]
# for i in range(len(RR)):
#     ActiveYearly=[]
#     TB_active=RR[i]
#     for i in range(0,len(TB_active),12):
#         aa=TB_active[i:i+11]
#         ActiveYearly.append(sum(aa))
#     Active_all.append(ActiveYearly)
#
# np.savetxt('Active_Yearly.txt' ,Active_all, delimiter=',')
# print "---", len(Active_all)
# Rows=range(len(Active_all))
# #Columns=range(12)
# Columns=range(len(ActiveYearly))
# dfarr=pd.DataFrame(data=Active_all, index=Rows,  columns=Columns)
# filename= './Active_all.csv'
# dfarr.to_csv(filename, sep=',')
#
#
# dfallstates = pd.DataFrame.from_csv('./Active_all.csv', sep=',')
#
# columns=list(dfallstates.columns.values)
#
# for i in columns:
#
#     eachcal=dfallstates[i].values
#
#     meanval.append(np.mean(eachcal))
#     stdval.append(np.std(eachcal))
#
#
# x = range(12)
# X=range(2004,2016)
# X=range(2004,2041)
#
# y = np.array(meanval)
# e = np.array(stdval)
#
# np.savetxt('./Ave_Active.txt',y , delimiter=',')
# print "---", len(X), len(y), len(e)
#
# plt.errorbar(X, y, e, linestyle='None', marker='^')
# plt.ylim(ymin=0)
# #ax0.errorbar(x, y, yerr=error, fmt='-o')
# plt.savefig('./Figures/Activeall_bar.pdf', format='pdf')
# plt.close()
# plt.clf()
#
#
#
# X1=range(2004,2041)
# X2=range(2004,2016)
#
# print "--- RP yearly compare ", y
# data_arrayx=[X1,X2]
# data_arrayy=[y, RCVT[0:12]]
# #data_array=[X,y, Control_TB_E]
# legends = ['Average model runs runs','Control data']
# text='./Figures/Ave_Active_Yearly_compare.pdf'
# plotter3.plot(text, data_arrayx, data_arrayy, legends, 'Years', 'Active cases')
#
#

X=range(2004,2016)
#X=range(2004,2040)
#print "--- ", len(X), len(RPyearly), len(RCVT), len(RPyearly[0:13]), len(RCVT[0:12])
data_array=[X,y[0:len(X)], RCVT[0:12]]
legends = ['Average of model runs','Control data']
text='./Figures/Ave_Active_Yearly_14.pdf'
plotter.plot(text, data_array, legends, 'Years', 'Active cases')
############################# recent transmission

RR=np.loadtxt('./All_Recent_Transimission.txt', dtype=None)

RT_all=[]
for i in range(len(RR)):
    RTYearly=[]
    TB_RT=RR[i]
    for i in range(0,len(TB_RT),12):
        aa=TB_RT[i:i+11]
        RTYearly.append(sum(aa))
    RT_all.append(RTYearly)

np.savetxt('RT_Yearly.txt' ,RT_all, delimiter=',')
#print "---", len(Active_all)
Rows=range(len(RT_all))
#Columns=range(12)
Columns=range(len(RTYearly))
dfarr=pd.DataFrame(data=RT_all, index=Rows,  columns=Columns)
filename= './RT_all.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./RT_all.csv', sep=',')

columns=list(dfallstates.columns.values)
meanval=[]
stdval=[]
for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


#x = range(12)
#X=range(2004,2016)
X=range(2004,2041)
yRC = np.array(meanval)
eRC = np.array(stdval)

np.savetxt('./Ave_RC.txt',yRC , delimiter=',')
#print "---", len(X), len(yRC), len(eRC)

plt.errorbar(X, yRC[0:len(X)], eRC[0:len(X)], linestyle='None', marker='^')
plt.ylim(ymin=0)
#ax0.errorbar(x, y, yerr=error, fmt='-o')
plt.savefig('./Figures/RTall_bar.pdf', format='pdf')
plt.close()
plt.clf()



X=range(2004,2016)
#X=range(2004,2040)
#print "--- ", len(X), len(RPyearly), len(RCVT), len(RPyearly[0:13]), len(RCVT[0:12])
data_array=[X,y[0:len(X)], yRC[0:len(X)],RCVT[0:12]]
legends = ['Active cases','Active cases by recent transmission','Control data']
text='./Figures/Ave_Active_RC_Yearly_14.pdf'
plotter.plot(text, data_array, legends, 'Years', 'Active cases')









################### TB_HIV

meanval=[]
stdval=[]

RR=np.loadtxt('./All_TB_HIV.txt')

TB_HIV_all_yearly=[]
for i in range(len(RR)):
    TBHIVYearly=[]
    TB_HIV_all=RR[i]
    for i in range(0,len(TB_HIV_all),12):
        aa=TB_HIV_all[i:i+11]
        TBHIVYearly.append(sum(aa))
    TB_HIV_all_yearly.append(TBHIVYearly)

np.savetxt('TB_HIV_Yearly.txt' ,TB_HIV_all_yearly, delimiter=',')
#print "---", len(Active_all)
Rows=range(len(TB_HIV_all_yearly))
Columns=range(len(TBHIVYearly))
dfarr=pd.DataFrame(data=TB_HIV_all_yearly, index=Rows,  columns=Columns)
filename= './TB_HIV_Yearly.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./TB_HIV_Yearly.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


#x = range(12)
y=[]
e=[]
X=range(2004,2068)
y = np.array(meanval)
e = np.array(stdval)

plt.close()
plt.clf()
# plt.errorbar(X, y, e, linestyle='None', marker='^')
# plt.ylim(ymin=0)
#ax0.errorbar(x, y, yerr=error, fmt='-o')
plt.savefig('./Figures/TB_HIV_bar.pdf', format='pdf')
plt.close()
plt.clf()


X1=range(2004,2068)
X2=range(2004,2016)

print "--- ", len(X1), len(y), len(X2),  len(RCVT[0:12])
data_arrayx=[X1,X2]
data_arrayy=[y, Control_TB_H]
#data_array=[X,y, Control_TB_E]
legends = ['Average of model runs','Control data']
text='./Figures/TB_HIV_compare_2040.pdf'
plotter3.plot(text, data_arrayx, data_arrayy, legends, 'Years', 'TB_HIV cases')



X1=range(2004,2016)
X2=range(2004,2016)

print "--- ", len(X1), len(y), len(X2),  len(RCVT[0:12])
data_arrayx=[X1,X2]
data_arrayy=[y[0:len(X1)], Control_TB_H]
#data_array=[X,y[0:len(X1)], Control_TB_H]
legends = ['Average of model runs','Control data']
text='./Figures/TB_HIV_compare.pdf'
plotter3.plot(text, data_arrayx, data_arrayy, legends, 'Years', 'TB_HIV cases')






################### TB_ESRD

meanval=[]
stdval=[]

RR=np.loadtxt('./All_TB_ESRD.txt')

TB_ESRD_all_yearly=[]
for i in range(len(RR)):
    TBESRDYearly=[]
    TB_ESRD_all=RR[i]
    for i in range(0,len(TB_ESRD_all),12):
        aa=TB_ESRD_all[i:i+11]
        TBESRDYearly.append(sum(aa))
    TB_ESRD_all_yearly.append(TBESRDYearly)

np.savetxt('TB_ESRD_Yearly.txt' ,TB_ESRD_all_yearly, delimiter=',')
#print "---", len(Active_all)
Rows=range(len(TB_ESRD_all_yearly))
Columns=range(len(TBESRDYearly))
dfarr=pd.DataFrame(data=TB_ESRD_all_yearly, index=Rows,  columns=Columns)
filename= './TB_ESRD_Yearly.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./TB_ESRD_Yearly.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


#x = range(12)
y=[]
e=[]
X=range(2004,2068)
y = np.array(meanval)
e = np.array(stdval)

plt.close()
plt.clf()
plt.errorbar(X, y, e, linestyle='None', marker='^')
plt.ylim(ymin=0)
#ax0.errorbar(x, y, yerr=error, fmt='-o')
plt.savefig('./Figures/TB_ESRD_bar.pdf', format='pdf')
plt.close()
plt.clf()

X1=range(2004,2068)
X2=range(2011,2016)
Control_TB_E=[82,87,84,74,82]
#print "--- ", len(X), len(RPyearly), len(RCVT), len(RPyearly[0:13]), len(RCVT[0:12])
data_arrayx=[X1,X2]
data_arrayy=[y, Control_TB_E]
#data_array=[X,y, Control_TB_E]
legends = ['Average of model runs','Control data']
text='./Figures/Ave_TB_ESRD_Yearly_2040.pdf'
plotter3.plot(text, data_arrayx, data_arrayy, legends, 'Years', 'TB_ESRD')


X1=range(2004,2016)
X2=range(2011,2016)
Control_TB_E=[82,87,84,74,82]
#print "--- ", len(X), len(RPyearly), len(RCVT), len(RPyearly[0:13]), len(RCVT[0:12])
data_arrayx=[X1,X2]
data_arrayy=[y[0:len(X1)], Control_TB_E]
#data_array=[X,y[0:len(X)], Control_TB_E]
legends = ['Average of model runs','Control data']
text='./Figures/Ave_TB_ESRD_Yearly.pdf'
plotter3.plot(text, data_arrayx, data_arrayy, legends, 'Years', 'TB_ESRD')





################### TB_Diabetes

meanval=[]
stdval=[]

RR=np.loadtxt('./All_TB_Diabetes.txt')

TB_Diabetes_all_yearly=[]
for i in range(len(RR)):
    TBDiabetesYearly=[]
    TB_Diabetes_all=RR[i]
    for i in range(0,len(TB_Diabetes_all),12):
        aa=TB_Diabetes_all[i:i+11]
        TBDiabetesYearly.append(sum(aa))
    TB_Diabetes_all_yearly.append(TBDiabetesYearly)

np.savetxt('TB_Diabetes_Yearly.txt' ,TB_Diabetes_all_yearly, delimiter=',')
#print "---", len(Active_all)
Rows=range(len(TB_Diabetes_all_yearly))
Columns=range(len(TBDiabetesYearly))
dfarr=pd.DataFrame(data=TB_Diabetes_all_yearly, index=Rows,  columns=Columns)
filename= './TB_Diabetes_Yearly.csv'
dfarr.to_csv(filename, sep=',')


dfallstates = pd.DataFrame.from_csv('./TB_Diabetes_Yearly.csv', sep=',')

columns=list(dfallstates.columns.values)

for i in columns:

    eachcal=dfallstates[i].values

    meanval.append(np.mean(eachcal))
    stdval.append(np.std(eachcal))


#x = range(12)
y=[]
e=[]
X=range(2004,2068)
y = np.array(meanval)
e = np.array(stdval)

plt.close()
plt.clf()
plt.errorbar(X, y, e, linestyle='None', marker='^')
plt.ylim(ymin=0)
#ax0.errorbar(x, y, yerr=error, fmt='-o')
plt.savefig('./Figures/TB_Diabetes_bar.pdf', format='pdf')
plt.close()
plt.clf()

X=range(2004,2016)
#print "--- ", len(X), len(RPyearly), len(RCVT), len(RPyearly[0:13]), len(RCVT[0:12])
data_array=[X,y[0:len(X)], Control_TB_D]
legends = ['Average of model runs','Control data']
text='./Figures/Ave_TB_Diabates_Yearly.pdf'
plotter.plot(text, data_array, legends, 'Years', 'TB_Diabetes')




X1=range(2004,2068)
X2=range(2011,2016)

Control_TB_D=[425,477,445,474,459]
print "--",len(X2),len(Control_TB_D)
data_arrayx=[X1,X2]
data_arrayy=[y,Control_TB_D]
#print "--- ", len(X), len(RPyearly), len(RCVT), len(RPyearly[0:13]), len(RCVT[0:12])
data_array=[X,y, Control_TB_D]
legends = ['Average of model runs','Control data']
text='./Figures/Ave_TB_Diabates_Yearly_2040.pdf'
plotter3.plot(text, data_arrayx, data_arrayy,legends, 'Years', 'TB_Diabetes')



X1=range(2004,2068)
X2=range(2011,2016)

Control_TB_D=[425,477,445,474,459]
print "--",len(X2),len(Control_TB_D)
data_arrayx=[X1,X2]
data_arrayy=[y[0:len(X1)],Control_TB_D]
#print "--- ", len(X), len(RPyearly), len(RCVT), len(RPyearly[0:13]), len(RCVT[0:12])
data_array=[X,y, Control_TB_D]
legends = ['Average of model runs','Control data']
text='./Figures/Ave_TB_Diabates_Yearly.pdf'
plotter3.plot(text, data_arrayx, data_arrayy,legends, 'Years', 'TB_Diabetes')
