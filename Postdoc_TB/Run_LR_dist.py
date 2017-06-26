#!/usr/bin/env python
#from  MC_array import *
#from MC_array_basecasea import *
#from MC_array_RR import *
from MC_array_RR import *
#from MC_array_RR_FB2x import *
#from MC_array_leave import *
#from MC_array_universaltesting import *
from Importdata_array import *

#from MC_cython_array import *
import time
import math
#from cython.parallel import prange
import numpy as np
#from pycallgraph import PyCallGraph
#from pycallgraph.output import GraphvizOutput
import pandas as pd
import resource
import os
#import psutil
#import plotter
from copy import deepcopy

path='./Results' #+ str(sys.argv[1])

#RCVT=[3085,2928,2967,2761,2733,2627,2570,2538,2328,2220,2191,2098,2070,2042] # 2002
RCVT=[2928,2967,2761,2733,2627,2570,2538,2328,2220,2191,2098,2070,2042] # 2003
# con = lite.connect('/Users/halehashki/Haleh/TB/limcat-master/database//limcat-zero-index.sqlite')
RT_RCVT=[551,496,451,414,382,355,331,311,292,276,262,249,237,226] ## from 2001

Control_TB_D=[0,0,0,0,0,0,0,425,477,445,474,459]
Control_TB_S=[0,0,0,0,0,0,0,118,226,229,258,264]
Control_TB_E=[0,0,0,0,0,0,0,82,87,84,74,82]
Control_TB_H=[185,139,148,153,141,136,109,101,101,88,76,86]




Riskfactor_id=[78,83,87,91,179,183,184,194,189,74,163,164,165,166,167,168,169,170,171,172]
Riskfactor_name=['Homeless','ESRD','TNF_alpha','Alcohol','Diabetes','HIV','HIV_ART','Transplant','IDU','Smoker','Age 35-39','Age 40-44','Age 45-49','Age 50-54','Age 55-59','Age 60-64','Age 65-69','Age 70-74','Age 75-79','Age 80+']


Susceptible_ActiveCase_dict={(0,'Asian'):0.0,(1,'Asian'):0.0, (0,'Black'):0.0,(1,'Black'):0.0, (0,'Hispanic'):0.0,(1,'Hispanic'):0.0, (0,'White'):0.0,(1,'White'):0.0, (0,'Other'):0.0,(1,'Other'):0.0}

People_ToState_Prob_dict={}
CalifoniaPopMonthly=np.loadtxt('./PopulationMonthly.txt', delimiter=',')

#PopulationNumber = [25534900.0,31206652.0] ### 2001,2014
PopulationNumber = [2.775998800000000000e+07,31206652.0] ### 2003,2014


Newcomers=np.loadtxt('./Newcommers.txt', delimiter=',')
Dead=0
percentage=100
cycle_duration=1 ### means 1 month duration or 2 or ...
cycle=144#320#444 # 144


TotalActiveCase=[0]

Activacase=[0] * cycle
ActivacaseRP=[0] * cycle
RPrate=[0]*cycle
SamplePopulation=[0]*cycle
LPR=[0]*cycle   ### In permanent resident and been tested before
Tested= [0]*cycle
AliveCal= [0]*cycle
Incidencerate=[0]*cycle
LTBI_SLOW=[0]*cycle
LTBI_FAST=[0]*cycle
FL_RPrate=[0]*cycle
FL_RPrate2=[0]*cycle

TB_D=[0.0]*cycle
TB_E=[0.0]*cycle
TB_H=[0.0]*cycle


RC_counter=[0]*cycle
RC_count=0
InitialFL=0
InitialFL_counter=[0]*cycle
##### Importing data and making all dictionaries

Variables=Make_Variables_dict()
Age_Group_Dict=Make_age_group_dict()

InteractionDict=Make_Interaction_states_dict()
Treatment_matrix=Make_Intervention_TP_dict(Variables)

VisaInfo=Visa_readfile()
#print "Visa info", VisaInfo


Intervention=Intervention_readfile_setupclass()


test_choice_pos=[]
test_choice_neg=[]
treatment_choice_pos=[]
treatment_choice_neg=[]
MonthlyUptake=[]



for i in xrange(len(Intervention)):
	test_choice_pos.append((Intervention[i].test_choice_pos).strip())
	test_choice_neg.append((Intervention[i].test_choice_neg).strip())
	treatment_choice_pos.append((Intervention[i].treatment_choice_pos).strip())
	treatment_choice_neg.append((Intervention[i].treatment_choice_neg).strip())
	#MonthlyUptake.append(float(Intervention[i].monthly_testing_uptake))
	##MonthlyUptake.append(float(0.00375))  ### 4.5% monthly 4.5/100/12
	MonthlyUptake.append(float(0.0016666))  ### 2% monthly 2/100/12





TP_dict,from_to_state_dict = Make_TransitionProb_FromTo_Dict()
TP_dict_ltbi=Make_TransitionProb_LTBI_FromTo_Dict()
STP_matrix=Make_TransitionProb_matrix()


InteractionAdjustDitc=Make_Interaction_Adjustment_dict( InteractionDict, Riskfactor_name, Riskfactor_id)
LifeDeath_Stratum_dict=Make_LifetoDeath_baseval_dict()

RiskFactor_StratumType_dict=Make_RiskFactor_StratumType_dict()
RiskFactor_TPvale_dict=Make_RiskFactor_Initialization()
Initial_People_Dict=Make_Base_init_dict()
PopSample_dict=Make_Population_Sample_dict()

begintime=time.time()
########Initializing People
# P=Initializing_people(PopSample_dict,round(PopulationNumber[0]/percentage),2,Riskfactor_id,Riskfactor_name,RiskFactor_TPvale_dict, Susceptible_ActiveCase_dict,RiskFactor_StratumType_dict,Initial_People_Dict,False)
# S_matrix, TP_matrix=first_cycle_LTBI(P,TP_dict_ltbi,1)
#
# P, Dead, RC_count, InitialFL =Assign_Next_Step(P, S_matrix, TP_matrix, Dead)
# RiskOfProgression,Susceptible_ActiveCase_dict, RT_RiskOfProgression =Cal_RiskOfProgression(1, P, S_matrix,TP_matrix,Susceptible_ActiveCase_dict)
# ActivacaseRP[0]= RiskOfProgression
#
#

RC_counter[0]=(RC_count)
InitialFL_counter[0]=(InitialFL)

#P[:,11]=P[:,11]+2
#P[:,11]=P[:,11]+1

RFD=[0]*cycle
RFS=[0]*cycle
RFE=[0]*cycle
RFH=[0]*cycle
RFT=[0]*cycle
RFTran=[0]*cycle
Death=[]
RiskAvg=[]
LEAVE=[0]*cycle



Chinees=[]
Indians=[]


AcceptVal_R=[]
AcceptVal_L=[]
AcceptVal_SL=[]
AcceptVal_RT_base=[]
AcceptVal_RT_L=[]
AcceptVal_TBE=[]
AcceptVal_TBD=[]
AcceptVal_TBH=[]
reject=True

# mcmcR=0.0022129338580365245
# mcmcL=0.04763246650914614
mcmcR=[0]*cycle
mcmcL=[0]*cycle

# for i in range(144):
# mcmcR=np.random.normal(0.00378,.00025,cycle)
# mcmcL=np.random.normal(0.0377,.00112,cycle)

#mcmcR[0:cycle]=np.random.normal(0.00378,.00025,cycle)
mcmcR[0:cycle]=np.random.normal(0.003489,8.65e-5,cycle)
#tt=(cycle-97) + 1
#mcmcR[97:cycle]=np.random.normal(0.003188,.0001146,tt)

#mcmcL[0:cycle]=np.random.normal(0.0377,.000254,cycle)
mcmcL[0:cycle]=np.random.normal(0.0382,.00055679,cycle)




#print "----- MCMCRL",mcmcR
# for i in range(48,144):
# 	mcmcR[i]=random.uniform(0.0,1.0)
# 	mcmcL[i]=random.uniform(0.0,1.0)


# mcmcR=0.0011
# mcmcL= 0.074

RT_base=2.37927555207
RT_L = -0.006910376469103505


mcmcTBD=2.7
mcmcTBE=19.78
mcmcTBH=16

mcmcSL=6.08536966506534e-05

#######new added

Susceptible_ActiveCase_dict = dict.fromkeys(Susceptible_ActiveCase_dict, 0.0)









#ActivacaseRP[0]= RiskOfProgression
#
# aliveP=len(P)
# Alivemonthly=CalifoniaPopMonthly[0] - LEAVE[0]
# AliveCal[0]= Alivemonthly
# RPrate[0]=float((ActivacaseRP[0] * Alivemonthly))/float(aliveP)
# #print "------", 0,  RPrate[0], ActivacaseRP[0] , Alivemonthly,aliveP
# Incidencerate[0]=RPrate[0]/float(aliveP)


P=Initializing_people(PopSample_dict,round(PopulationNumber[0]/percentage),2,Riskfactor_id,Riskfactor_name,RiskFactor_TPvale_dict, Susceptible_ActiveCase_dict,RiskFactor_StratumType_dict,Initial_People_Dict,False)
S_matrix, TP_matrix=first_cycle_LTBI(P,TP_dict_ltbi,1)

P, Dead, RC_count, InitialFL =Assign_Next_Step(P, S_matrix, TP_matrix, Dead)

Alivemonthly=CalifoniaPopMonthly[0]


A=P[:,0:30]

Rows=range(len(P))
#Columns=range(28)
Columns=range(30)
dfarr=pd.DataFrame(data=A, index=Rows,  columns=Columns)

filename=path + '/PeoplesInfo.csv'
dfarr.to_csv(filename, sep=',')
##### Initail risk factors
A=P[:,15:25]

Rows=range(A.shape[0])
Columns=range(A.shape[1])
dfarr=pd.DataFrame(data=A, index=Rows,  columns=Columns)
filename=path + '/PeoplesRiskFactors.csv'
dfarr.to_csv(filename, sep=',')

PopKeys=[(0,'Asian'),(1,'Asian'), (0,'Black'),(1,'Black'), (0,'Hispanic'),(1,'Hispanic'), (0,'White'),(1,'White'), (0,'Other'),(1,'Other')]
A=[[0]*cycle for i in range(10)]

AcceptVal_R=[]
AcceptVal_L=[]
AcceptVal_SL=[]
reject=True



RejectCounter=0
begintime=time.time()
#print "++++++ PRate",  RPrate
# gviz = GraphvizOutput()
# gviz.output_file = "basic.png"
# with PyCallGraph(output=gviz):


ci=-1
#for ci in range(2,cycle):
oldP=P
while ci < cycle-1:
    #print "++++++ PRate", ci,  RPrate
    reject=True
    ci=ci+1



    if ci==1 :
		#oldP=P[:]
		oldP=deepcopy(P)


    RiskOfProgression=0
    SamplePopulation[ci]=len(P)

    aa=np.where(P[:,27] == 1)
    aliveP=len(aa[0])

    print "-------------------------------------------------------------------------------------------------------", ci, len(P),RPrate[ci-1]

    #if ci <= 360: # and (ci%12) == 0:
		#Cyclecounter=Cyclecounter+1
    numberofnewcomers=round((Newcomers[ci/12]/percentage)/12)



	#numberofnewcomers=round((Newcomers[Cyclecounter]/percentage))
	############TO TSETTTTTTTTTTT
    P1=Initializing_people(PopSample_dict,numberofnewcomers,ci,Riskfactor_id,Riskfactor_name,RiskFactor_TPvale_dict, Susceptible_ActiveCase_dict,RiskFactor_StratumType_dict,Initial_People_Dict,True)
    S_matrix,TP_matrix = first_cycle_LTBI(P1,TP_dict_ltbi,ci)
    P1, Dead , RC_count ,InitialFL=Assign_Next_Step(P1, S_matrix, TP_matrix,Dead)
    hhh=np.where(P1[:,11]==1)

    InitialFL_counter[ci]=(float((InitialFL * Alivemonthly))/float(aliveP))



    P=np.concatenate((P,P1), axis=0)
	###############TO TESTTTTTTTT
	#### keep the old P for MCMC
	# if (ci%12) == 0: ## every year
	# 	OldP=P


    hhh=np.where(np.logical_and(P[:,11]==1,P[:,27]==1))




    ActivacaseRPval=ActivacaseRP[ci-1]
    S_matrix, TP_matrix, RiskAverage,Tested[ci],LTBI_SLOW[ci], LTBI_FAST[ci], Fast_RP  =Make_Next_Step_Matrix(P,ci, Intervention,STP_matrix,Treatment_matrix,ActivacaseRPval,Susceptible_ActiveCase_dict,test_choice_pos,test_choice_neg,treatment_choice_pos,treatment_choice_neg,MonthlyUptake,VisaInfo,LPR[ci-1],mcmcR[ci], mcmcL[ci], mcmcSL, RT_base,RT_L, mcmcTBD, mcmcTBE, mcmcTBH)
    #Susceptible_ActiveCase_dict = dict.fromkeys(Susceptible_ActiveCase_dict, [0,0.0])
    Susceptible_ActiveCase_dict = dict.fromkeys(Susceptible_ActiveCase_dict, 0.0)


    P,Dead, RC_count, InitialFL =Assign_Next_Step(P, S_matrix, TP_matrix,Dead)
    LL=np.where(P[:,27]==0)
    #RC_counter.append(RC_count)
    RC_counter[ci]=(float((RC_count * Alivemonthly))/float(aliveP))

    #print "leave", len (LL[0])
    #LEAVE[ci]= len(LL[0])
    LEAVE[ci]=(float((len(LL[0]) * CalifoniaPopMonthly[ci]))/float(len(P)))

    RiskOfProgression,Susceptible_ActiveCase_dict , RT_RiskOfProgression,TB_Diabetes, TB_ESRD, TB_HIV =Cal_RiskOfProgression(ci, P, S_matrix,TP_matrix,Susceptible_ActiveCase_dict)
    ActivacaseRP[ci]= RiskOfProgression
    Alivemonthly=CalifoniaPopMonthly[ci] - LEAVE[ci]
    AliveCal[ci]= Alivemonthly
    RPrate[ci]=float((ActivacaseRP[ci] * Alivemonthly))/float(aliveP)

    FL_RPrate[ci]=float((Fast_RP * Alivemonthly))/float(aliveP)

    FL_RPrate2[ci]=float((RT_RiskOfProgression * Alivemonthly))/float(aliveP)



    Incidencerate[ci]=RPrate[ci]/float(aliveP)
    #print "------", ci ,ActivacaseRP[ci], ActivacaseRP[ci] ,Alivemonthly,aliveP,RPrate[ci]

    TB_D[ci]= float((TB_Diabetes * Alivemonthly))/float(aliveP)
    TB_E[ci]=float((TB_ESRD * Alivemonthly))/float(aliveP)
    TB_H[ci]=float((TB_HIV * Alivemonthly))/float(aliveP)
    # print "----- RR", RiskOfProgression, TB_Diabetes, TB_ESRD, TB_HIV, "----", RPrate[ci],TB_D[ci],TB_E[ci],TB_H[ci]
    # print "+++++++++++++", TB_D,TB_E,TB_H
    #print "---- RP and Diabetes, Smoking, HIV", ci, RPrate[ci], TB_D[ci],TB_E[ci],TB_H[ci]
    P=Active_Case_Finding(P,ci, ActivacaseRP,     Intervention)
    P,Dead=Update_Cycle(P,ci,LifeDeath_Stratum_dict,InteractionAdjustDitc,Age_Group_Dict,Dead)
    P=Outgoing_pop(P)
    P, LPR[ci]=Visa_Status_Change(P,ci)
    P=Visa_Status_Leave(P)



    RFDiabetes=len(np.where(np.logical_and(P[:,23]==1,P[:,27]==1))[0])
    RFD[ci]=RFDiabetes
    RFSmokers=len(np.where(np.logical_and(P[:,24]==1,P[:,27]==1))[0])
    RFS[ci]=RFSmokers
    RFESRD=len(np.where(np.logical_and(P[:,16]==1,P[:,27]==1))[0])
    RFE[ci]=RFESRD

    RFHIV1=len(np.where(np.logical_and(P[:,19]==1,P[:,27]==1))[0])
    RFHIV2=len(np.where(np.logical_and(P[:,20]==1,P[:,27]==1))[0])
    RFH[ci]=RFHIV1+RFHIV2
    RFTNF=len(np.where(np.logical_and(P[:,17]==1,P[:,27]==1))[0])
    RFT[ci]=RFTNF
    RFTransplant=len(np.where(np.logical_and(P[:,21]==1,P[:,27]==1))[0])
    RFTran[ci]=RFTransplant
    Death.append(float((Dead * CalifoniaPopMonthly[ci]))/float(len(P)))

    RiskAvg.append((float((RiskAverage * Alivemonthly))/float(aliveP)))

	#
    # if ci < 14: ## 48 for having relaxed MCMC
	# ##Markov process
	#     if (ci%12) == 1 and ci >12: ## every year , 13, 25 ,...
	#
	# 		### RPyearly[0:13], RCVT[1:14]]   RCVT and RPrate calculated for yearly
	# 		## RP in accpetance range  caluclate the margine of error for RCVT and then compare the result with
	# 		### for test
	#
	#         aa=RPrate[ci-11:ci+1]
	#         #print "====== MCMC ",  ci-11, ci+1, aa, sum(aa)
	#         RPyearly=(sum(aa))
	#
	#         yearno=ci/12
	# 	RCVTyearly=RCVT[yearno]
    #         	print "================= into check ", ci, RCVTyearly,RPyearly
	# 	if abs(RCVTyearly-RPyearly) < 50 : #and abs(RF_H - Control_TB_H[yearno]) < 70 : ## < mcmcr and RC_RCVTyearly/FL_RPyearly  >= .8:  ## ??????? PETER should i accept if feel in margine or have random number in margine to accept or reject
	# 		reject =False
	#
	#
	#
	#
	#         if reject:
	#
	#
	# 		#mcmcR[0:14]=np.random.normal(0.00378,.00025,14)
	#
	# 		mcmcR[0:14]=np.random.normal(0.0035268,.0001328,14)
	# 		mcmcL[0:14]=np.random.normal(0.0377,.000254,14)
	#
	#
	# 		ci=ci-12
	# 	        P=deepcopy(oldP)
	#
	#
    #             	print "--------------------------------------------------------------- Reject ", ci, yearno, RPyearly,RCVTyearly,mcmcR[ci],mcmcL[ci]
	#
	#
	#         else:
	#
	# 			oldP=deepcopy(P)
	#
	# 			print "++++++++++ Accept ",  ci, yearno, RPyearly,RCVTyearly,mcmcR[ci],mcmcL[ci]
	# 			AcceptVal_R.append(mcmcR)
	# 			AcceptVal_L.append(mcmcL)
	# 			#print "Accept", ci
	#
	#
	#
	#






    #### RiskFactor prevelance
    # RFDiabetes=len(np.where(np.logical_and(P[:,23]==1,P[:,27]==1))[0])
    # RFD[ci]=RFDiabetes
    # RFSmokers=len(np.where(np.logical_and(P[:,24]==1,P[:,27]==1))[0])
    # RFS[ci]=RFSmokers
    # RFESRD=len(np.where(np.logical_and(P[:,16]==1,P[:,27]==1))[0])
    # RFE[ci]=RFESRD
	#
    # RFHIV1=len(np.where(np.logical_and(P[:,19]==1,P[:,27]==1))[0])
    # RFHIV2=len(np.where(np.logical_and(P[:,20]==1,P[:,27]==1))[0])
    # RFH[ci]=RFHIV1+RFHIV2
    # RFTNF=len(np.where(np.logical_and(P[:,17]==1,P[:,27]==1))[0])
    # RFT[ci]=RFTNF
    # RFTransplant=len(np.where(np.logical_and(P[:,21]==1,P[:,27]==1))[0])
    # RFTran[ci]=RFTransplant
    # Death.append(float((Dead * CalifoniaPopMonthly[ci]))/float(len(P)))
	#
    # RiskAvg.append((float((RiskAverage * Alivemonthly))/float(aliveP)))

	### TB +Risk factors
    # TB_D.append(TB_Diabetes)
    # TB_S.append(TB_Smoking)
    # TB_H.append(TB_HIV)


    b=np.where(P[:,27]==1)
    PP=P[b[0],:]
    mykeys=zip(PP[:,7],PP[:,2])
    cc = Counter(mykeys)


    counter=-1
    for j in PopKeys:
        counter=counter+1
        aa= np.multiply(cc[j], CalifoniaPopMonthly[ci])
        Y=np.divide(aa,len(P))

        A[counter][ci]=Y




	# print "ci before", ci
	# ci=ci+1  ## for while
	# print "ci after", ci

Rows=range(10)
Columns=range(cycle)
dfarr=pd.DataFrame(data=A, index=Rows,  columns=Columns)
filename=path + '/RaceEthnicity.csv'
dfarr.to_csv(filename, sep=',')



endtime=time.time()
runtime=endtime-begintime
print " minutes, seconds" , runtime // 60, runtime % 60


filename=path + '/RiskOfProgression.txt'
#print filename
#filename=str(path) + '/RiskOfProgression.txt'
np.savetxt(filename, ActivacaseRP, delimiter=',')
filename=path + '/RFDiabetes.txt'
np.savetxt(filename, RFD, delimiter=',')
filename=path + '/RFSmokers.txt'
np.savetxt(filename, RFS, delimiter=',')
filename=path + '/RFESRD.txt'
np.savetxt(filename, RFE, delimiter=',')
filename=path + '/RFHIV.txt'
np.savetxt(filename, RFH, delimiter=',')
filename=path + '/RFTNFalpha.txt'
np.savetxt(filename, RFT, delimiter=',')
filename=path + '/RFTransplant.txt'
np.savetxt(filename, RFTran, delimiter=',')
filename=path + '/SamplePopulation.txt'
np.savetxt(filename, SamplePopulation, delimiter=',')
filename=path + '/RPrate.txt'
np.savetxt(filename, RPrate, delimiter=',')
filename=path + '/RiskAverage.txt'
np.savetxt(filename, RiskAvg, delimiter=',')
filename=path + '/Deadrate.txt'
np.savetxt(filename, Death, delimiter=',')
filename=path + '/Incidencerate.txt'
np.savetxt(filename, Incidencerate, delimiter=',')

filename=path + '/LTBISlowLatent.txt'
np.savetxt(filename, LTBI_SLOW, delimiter=',')

filename=path + '/LTBIFastLatent.txt'
np.savetxt(filename, LTBI_FAST, delimiter=',')

filename=path + '/FL_RecentTransmission.txt'
np.savetxt(filename, FL_RPrate, delimiter=',')


filename=path + '/FL_RecentTransmission2.txt'
np.savetxt(filename, FL_RPrate2, delimiter=',')

filename=path + '/TB_HIV.txt'
np.savetxt(filename, TB_H, delimiter=',')

filename=path + '/TB_Diabetes.txt'
np.savetxt(filename, TB_D, delimiter=',')


filename=path + '/TB_ESRD.txt'
np.savetxt(filename, TB_E, delimiter=',')



# print "----------------- RP active cases", ActivacaseRP
print "----------------- RP active cases", RPrate
# print "__________________ TESTED ", Tested
# print "___________________ LPR", LPR

filename=path + '/Tested.txt'
np.savetxt(filename, Tested, delimiter=',')
filename=path + '/LPR.txt'
np.savetxt(filename, LPR , delimiter=',')

AA=P[:,0:30]

Rows=range(len(P))
#Columns=range(11)
Columns=range(30)
dfarr=pd.DataFrame(data=AA, index=Rows,  columns=Columns)

filename=path + '/FinalPeoplesInfo.csv'
dfarr.to_csv(filename, sep=',')




#######All states



B=np.zeros(shape= (len(P), cycle), dtype='int32')


for i in range(len(P)-1):
	A=np.array(P[i,14])
	if A.shape[0] != B[i,:].shape[0]:
		##print " yeki nist ", A.shape[0],  B[i,:].shape[0], len(A[0:B.shape[1]])
		temp=A[0:B.shape[1]]
		A=temp

	B[i,:]=A



Rows=range(B.shape[0])
Columns=range(B.shape[1])
dfarr=pd.DataFrame(data=B, index=Rows,  columns=Columns)
filename=path + '/Allstates.csv'
dfarr.to_csv(filename, sep=',')
print "RPrate", RPrate


print "recent transmission ", FL_RPrate
filename=path + '/Recent_transmission_count.txt'
np.savetxt(filename, FL_RPrate, delimiter=',')


print "reject number", RejectCounter
print "Accpeted MCMC vals R ", AcceptVal_R
print "Accpeted MCMC vals L ",AcceptVal_L

print "Fast latent", AcceptVal_RT_base
print "Slow latent", AcceptVal_RT_L
#print AcceptVal_SL

filename=path + '/AcceptVal_L.txt'
np.savetxt(filename, AcceptVal_L, delimiter=',')
filename=path + '/AcceptVal_R.txt'
np.savetxt(filename, AcceptVal_R , delimiter=',')

filename=path + '/AcceptVal_TBD.txt'
np.savetxt(filename, AcceptVal_TBD, delimiter=',')


filename=path + '/AcceptVal_TBE.txt'
np.savetxt(filename, AcceptVal_TBE, delimiter=',')


filename=path + '/AcceptVal_TBH.txt'
np.savetxt(filename, AcceptVal_TBH, delimiter=',')



filename=path + '/ZeroToTwo.txt'
np.savetxt(filename, InitialFL_counter, delimiter=',')

filename=path + '/OneToTwo.txt'
np.savetxt(filename, RC_counter, delimiter=',')

####for i in `seq 1 4`; do qsub myscript.q; done
