#!/usr/bin/env python
from  Importdata_array import *
from  MC_array_bk import *
#from MC_cython_array import *
import time
#from cython.parallel import prange
import numpy as np
#import pandas as pd

# con = lite.connect('/Users/halehashki/Haleh/TB/limcat-master/database//limcat-zero-index.sqlite')

import resource
import os
import psutil

def memory_usage_psutil():
    # return the memory usage in percentage like top
    #import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_percent()
    return mem





Riskfactor_id=[78,83,87,91,179,183,184,194,189,74,163,164,165,166,167,168,169,170,171,172]
Riskfactor_name=['Homeless','ESRD','TNF_alpha','Alcohol','Diabetes','HIV','HIV_ART','Transplant','IDU','Smoker','Age 35-39','Age 40-44','Age 45-49','Age 50-54','Age 55-59','Age 60-64','Age 65-69','Age 70-74','Age 75-79','Age 80+']


# Susceptible_ActiveCase_dict={('0','Asian'):[0,0.0],('1','Asian'):[0,0.0], ('0','Black'):[0,0.0],('1','Black'):[0,0.0], ('0','Hispanic'):[0,0.0],('1','Hispanic'):[0,0.0], ('0','White'):[0,0.0],('1','White'):[0,0.0], ('0','Other'):[0,0.0],('1','Other'):[0,0.0]}
#Susceptible_ActiveCase_dict={(0,'Asian'):[0,0.0],(1,'Asian'):[0,0.0], (0,'Black'):[0,0.0],(1,'Black'):[0,0.0], (0,'Hispanic'):[0,0.0],(1,'Hispanic'):[0,0.0], (0,'White'):[0,0.0],(1,'White'):[0,0.0], (0,'Other'):[0,0.0],(1,'Other'):[0,0.0]}
Susceptible_ActiveCase_dict={(0,'Asian'):0.0,(1,'Asian'):0.0, (0,'Black'):0.0,(1,'Black'):0.0, (0,'Hispanic'):0.0,(1,'Hispanic'):0.0, (0,'White'):0.0,(1,'White'):0.0, (0,'Other'):0.0,(1,'Other'):0.0}

People_ToState_Prob_dict={}
CalifoniaPopMonthly=[34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34490000, 34522500, 34555000, 34587500, 34620000, 34652500, 34685000, 34717500, 34750000, 34782500, 34815000, 34847500, 34880000, 34910833, 34941666, 34972499, 35003332, 35034165, 35064998, 35095831, 35126664, 35157497, 35188330, 35219163, 35250000, 35275833, 35301666, 35327499, 35353332, 35379165, 35404998, 35430831, 35456664, 35482497, 35508330, 35534163, 35560000, 35595000, 35630000, 35665000, 35700000, 35735000, 35770000, 35805000, 35840000, 35875000, 35910000, 35945000, 35980000, 36000833, 36021666, 36042499, 36063332, 36084165, 36104998, 36125831, 36146664, 36167497, 36188330, 36209163, 36230000, 36259166, 36288332, 36317498, 36346664, 36375830, 36404996, 36434162, 36463328, 36492494, 36521660, 36550826, 36580000, 36611666, 36643332, 36674998, 36706664, 36738330, 36769996, 36801662, 36833328, 36864994, 36896660, 36928326, 36960000, 36991666, 37023332, 37054998, 37086664, 37118330, 37149996, 37181662, 37213328, 37244994, 37276660, 37308326, 37340000, 37368333, 37396666, 37424999, 37453332, 37481665, 37509998, 37538331, 37566664, 37594997, 37623330, 37651663, 37680000, 37706666, 37733332, 37759998, 37786664, 37813330, 37839996, 37866662, 37893328, 37919994, 37946660, 37973326, 38000000, 38027500, 38055000, 38082500, 38110000, 38137500, 38165000, 38192500, 38220000, 38247500, 38275000, 38302500, 38330000, 38369166, 38408332, 38447498, 38486664, 38525830, 38564996, 38604162, 38643328, 38682494, 38721660, 38760826]

PopulationNumber = [25534900.0,31206652.0] ### 2001,2014
#Newcomers=[569885.0,526445.0,548132.0,591289.0,619247.0,632620.0,611119.0,577231.0,550541.0,583596.0,569812.0,559316.0,568943.0,564637.0]   ####2001-2014
Newcomers=[1163173.0,1100130.0,1103093.0,1127722.0,1161383.0,1259438.0,1205765.0,1183370.0,1114440.0,1141379.0,1149439.0,1163563.0,1171139.0,1188697.0]

Dead=0
percentage=1000
#PopulationNumber=1000
cycle_duration=1 ### means 1 month duration or 2 or ...
cycle=50


TotalActiveCase=[0]

Activacase=[0] * cycle
ActivacaseRP=[0] * cycle
RPrate=[0]*cycle
SamplePopulation=[0]*cycle

##### Importing data and making all dictionaries

Variables=Make_Variables_dict()
Age_Group_Dict=Make_age_group_dict()

InteractionDict=Make_Interaction_states_dict()
Treatment_matrix=Make_Intervention_TP_dict(Variables)


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
	MonthlyUptake.append(float(Intervention[i].monthly_testing_uptake))

print "TT ", test_choice_pos,test_choice_neg,treatment_choice_pos,treatment_choice_neg,MonthlyUptake


TP_dict,from_to_state_dict = Make_TransitionProb_FromTo_Dict()
STP_matrix=Make_TransitionProb_matrix()


InteractionAdjustDitc=Make_Interaction_Adjustment_dict( InteractionDict, Riskfactor_name, Riskfactor_id)
#print "$$$$$$$", InteractionAdjustDitc
LifeDeath_Stratum_dict=Make_LifetoDeath_baseval_dict()

##RiskFactor_MonthlyChance=Make_monthly_RiskFactor_chance_dict()
RiskFactor_StratumType_dict=Make_RiskFactor_StratumType_dict()
RiskFactor_TPvale_dict=Make_RiskFactor_Initialization()
#intvsample=[i for i in range(len(Intervention))]
Initial_People_Dict=Make_Base_init_dict()


#TP_matrix= Make_TransitionProb_matrix()
begintime=time.time()
########Initializing People
P=Initializing_people(round(PopulationNumber[0]/percentage),2,Riskfactor_id,Riskfactor_name,RiskFactor_TPvale_dict, Susceptible_ActiveCase_dict,RiskFactor_StratumType_dict,Initial_People_Dict,False)
S_matrix, TP_matrix=first_cycle(P,TP_dict)
P, Dead=Assign_Next_Step(P, S_matrix, TP_matrix, Dead)

RFD=[]
RFS=[]
RFE=[]
RFH=[]
RFT=[]
RFTran=[]
Death=[]
RiskAvg=[]




# ###INitial people's information
# A=P[:,0:11]
#
# Rows=range(len(P))
# Columns=range(11)
# dfarr=pd.DataFrame(data=A, index=Rows,  columns=Columns)
#
# dfarr.to_csv('./Plots/Results/PeoplesInfo.csv', sep=',')
# ##### Initail risk factors
# A=P[:,15:25]

# Rows=range(A.shape[0])
# Columns=range(A.shape[1])
# dfarr=pd.DataFrame(data=A, index=Rows,  columns=Columns)
# dfarr.to_csv('./Plots/Results/PeoplesRiskFactors.csv', sep=',')
#


begintime=time.time()
for ci in range(2,cycle):
	RiskOfProgression=0
	SamplePopulation[ci]=len(P)

	print "--------------------------------------------------------------------------------------------------", ci,len(P)
	#print  memory_usage_psutil()
	if ci <= 156:
		numberofnewcomers=round((Newcomers[ci/12]/percentage)/12)
		P1=Initializing_people(numberofnewcomers,ci,Riskfactor_id,Riskfactor_name,RiskFactor_TPvale_dict, Susceptible_ActiveCase_dict,RiskFactor_StratumType_dict,Initial_People_Dict,True)
		S_matrix, TP_matrix=first_cycle(P1,TP_dict)
		P1, Dead =Assign_Next_Step(P1, S_matrix, TP_matrix,Dead)
		P=np.concatenate((P,P1), axis=0)
		#print "len P ", len(P)
	else:
		numberofnewcomers=round((Newcomers[13]/percentage)/12) ### meaning the same as 2014
		P1=Initializing_people(numberofnewcomers,ci,Riskfactor_id,Riskfactor_name,RiskFactor_TPvale_dict, Susceptible_ActiveCase_dict,RiskFactor_StratumType_dict,Initial_People_Dict,True)
		S_matrix, TP_matrix=first_cycle(P1,TP_dict)
		P1,Dead=Assign_Next_Step(P1, S_matrix, TP_matrix,Dead)
		P=np.concatenate((P,P1), axis=0)
		#print "len P ", len(P)

	##Markov process
	ActivacaseRPval=ActivacaseRP[ci-1]
	S_matrix, TP_matrix, RiskAverage=Make_Next_Step_Matrix(P,ci, Intervention,STP_matrix,Treatment_matrix,ActivacaseRPval,Susceptible_ActiveCase_dict,test_choice_pos,test_choice_neg,treatment_choice_pos,treatment_choice_neg,MonthlyUptake)
	#Susceptible_ActiveCase_dict = dict.fromkeys(Susceptible_ActiveCase_dict, [0,0.0])
	Susceptible_ActiveCase_dict = dict.fromkeys(Susceptible_ActiveCase_dict, 0.0)


	P,Dead=Assign_Next_Step(P, S_matrix, TP_matrix,Dead)
	RiskOfProgression,Susceptible_ActiveCase_dict=Cal_RiskOfProgression(P, S_matrix,TP_matrix,Susceptible_ActiveCase_dict)
	ActivacaseRP[ci]= RiskOfProgression
	RPrate[ci]=float((ActivacaseRP[ci] * CalifoniaPopMonthly[ci]))/float(len(P))
	P=Active_Case_Finding(P,ci, ActivacaseRP,     Intervention)
 	P,Dead=Update_Cycle(P,ci,LifeDeath_Stratum_dict,InteractionAdjustDitc,Age_Group_Dict,Dead)
	#### RiskFactor prevelance
	# RFDiabetes=len(np.where(np.logical_and(P[:,23]==1,P[:,27]==1))[0])
	# RFD.append(RFDiabetes)
	# RFSmokers=len(np.where(np.logical_and(P[:,24]==1,P[:,27]==1))[0])
	# RFS.append(RFSmokers)
	# RFESRD=len(np.where(np.logical_and(P[:,16]==1,P[:,27]==1))[0])
	# RFE.append(RFESRD)
	# RFHIV=len(np.where(np.logical_and(P[:,19]==1,P[:,27]==1))[0])
	# RFH.append(RFHIV)
	# RFTNF=len(np.where(np.logical_and(P[:,17]==1,P[:,27]==1))[0])
	# RFT.append(RFTNF)
	# RFTransplant=len(np.where(np.logical_and(P[:,21]==1,P[:,27]==1))[0])
	# RFTran.append(RFTransplant)
	# Death.append(float((Dead * CalifoniaPopMonthly[ci]))/float(len(P)))
	# RiskAvg.append(RiskAverage)





endtime=time.time()
runtime=endtime-begintime
print " minutes, seconds" , runtime // 60, runtime % 60

# np.savetxt('./Plots/Results/RiskOfProgression.txt', ActivacaseRP, delimiter=',')
# np.savetxt('./Plots/Results/RFDiabetes.txt', RFD, delimiter=',')
# np.savetxt('./Plots/Results/RFSmokers.txt', RFS, delimiter=',')
# np.savetxt('./Plots/Results/RFESRD.txt', RFE, delimiter=',')
# np.savetxt('./Plots/Results/RFHIV.txt', RFH, delimiter=',')
# np.savetxt('./Plots/Results/RFTNFalpha.txt', RFT, delimiter=',')
# np.savetxt('./Plots/Results/RFTransplant.txt', RFTran, delimiter=',')
# np.savetxt('./Plots/Results/SamplePopulation.txt', SamplePopulation, delimiter=',')
# np.savetxt('./Plots/Results/RPrate.txt', RPrate, delimiter=',')
# np.savetxt('./Plots/Results/RiskAverage.txt', RiskAvg, delimiter=',')
# np.savetxt('./Plots/Results/Deadrate.txt', Death, delimiter=',')
#


#######All states


#filename = open('./Plots/Results/Allstates.txt', 'w')
#B=np.zeros(shape= (len(P), cycle), dtype='int32')
#A=np.array(P[1,14])
#print "===", cycle, len(P[1,14])

# for i in range(len(P)-1):
# 	A=np.array(P[i,14])
# 	if A.shape[0] != B[i,:].shape[0]:
# 		print " yeki nist ", A.shape[0],  B[i,:].shape[0], len(A[0:B.shape[1]])
# 		temp=A[0:B.shape[1]]
# 		A=temp
#
# 	B[i,:]=A



# Rows=range(B.shape[0])
# Columns=range(B.shape[1])
# dfarr=pd.DataFrame(data=B, index=Rows,  columns=Columns)
# dfarr.to_csv('./Plots/Results/Allstates.csv', sep=',')



#print "----------------- RP active cases", ActivacaseRP
print "----------------- RP active cases", RPrate
# for i in range(len(P)):
# 	print P[i][14]
#

###Final people's information
# A=P[:,0:11]
#
# Rows=range(len(P))
# Columns=range(11)
# dfarr=pd.DataFrame(data=A, index=Rows,  columns=Columns)
#
# dfarr.to_csv('./Plots/Results/FinalPeoplesInfo.csv', sep=',')
