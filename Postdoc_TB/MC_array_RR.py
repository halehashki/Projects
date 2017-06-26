#!/usr/bin/env python

import sqlite3 as lite
import random
import numpy as np
import time
import math

from collections import Counter
#from Collections import Counter
#import Counter


def Make_Next_Step_Matrix(P,ci, Intervention,STP_matrix,Treatment_matrix,ActivacaseRPval,Susceptible_ActiveCase_dict,test_choice_pos,test_choice_neg,treatment_choice_pos,treatment_choice_neg,MonthlyUptake,VisaInerven,LPRtested, mcmcR, mcmcL, mcmcSL,RT_base,RT_L, mcmcTBD, mcmcTBE, mcmcTBH):
	Ntested=0
	visaclass= int(VisaInerven[4]) ### check which index it is
	visasample=VisaInerven[5]
	visaTpos=VisaInerven[0]
	visaTneg=VisaInerven[1]
	countryname= VisaInerven[6]

	#Palive=np.where(P[:,27]==1)
	tt1=0
	tt2=0
	tt3=0
	tt4=0

	S_matrix=np.zeros((len(P),5), dtype='float64')
	TP_matrix=np.zeros((len(P),5), dtype='float64')

	b=np.where(np.logical_and(P[:,8]==1,P[:,27]==1)) ### state=1

	#### Transmission calculation
	totalSusceptible = len(b[0])

	totalActive= ActivacaseRPval
	generalPopulationRisk = float(float(totalActive / totalSusceptible) * 0.2)
	#generalPopulationRisk = float(float(totalActive / totalSusceptible) * 0.5)


	Tneg=[0,0]
	Tpos=[0,0]
	Uptake=[0.0,0.0]
	risk=0.0


	#### person in state 1 has porbability of uptake value to be choosen for test


	begintime=time.time()
	mykeys=zip(P[b[0],7],P[b[0],2])

	#####COUNT THE NUMBER OF SUSCEPTIBLE FOR EACH GROUP
	c = Counter(mykeys)
	#print "mykeys, c", mykeys, c

	counter=-1
	#### use np.zeros instead

	susceptiblearr=[0]*len(b[0])
	for i in mykeys:
		counter=counter+1
		susceptiblearr[counter]=c[i]

	activearr=np.asarray([Susceptible_ActiveCase_dict[x] for x in mykeys])
	#print "++++ activearr", activearr


	a1=np.divide(activearr,susceptiblearr)
	#print "+++++=====", a1
	a2=np.multiply(a1,0.8)
	#a2=np.multiply(a1,0.5)
	a3=np.add(a2,generalPopulationRisk)
	#Risklist1=np.multiply(a3,4.0)
	Risklist=np.multiply(a3,4.0)
	#Risklist=np.multiply(a3,3.0)




	##### dynamic transmission rate
	#print "-- ci", ci, math.exp (-.0025 * ci)
	#tr_factor=1.5 * math.exp (-.00422 * ci) # for 8 Years
	#tr_factor=RT_base * math.exp (RT_L * ci)
	#tr_factor=1.5 * math.exp (-0.0024 * ci)## for 14 years
	#tr_factor=1.14 * math.exp (-0.013 * ci) ## MCMC val
	#tr_factor=3.5 * math.exp (-.013 * ci)

	# if ci < 48: ### no MCMC
	# 	tr_factor=1
	#
	# Risklist=np.multiply(Risklist1,tr_factor)

	#print "------ MCMC ", Risklist1, tr_factor, Risklist
	RiskAverage=sum(Risklist) #(sum(Risklist) / float(len(Risklist)))
	#print "SUm of all 1 to 2", RiskAverage

	S_matrix[b[0],0]=Tneg[0] ## first element is uptake value for test
	S_matrix[b[0],1]=Tneg[1]
	S_matrix[b[0],2]=1
	S_matrix[b[0],3]=2

	TP_matrix[b[0],0]=Uptake[0] ## first element is uptake value for test
	TP_matrix[b[0],1]=Uptake[1]
	TP_matrix[b[0],2]=.99
	TP_matrix[b[0],3]=Risklist
	#TP_matrix[b[0],3]=.000001


	###############for people in state 2, only goes to 2 and 63, test
	b=np.where(np.logical_and(P[:,8]==2, P[:,27] ==1)) ### state=2

	Tpos=[0,0]
	Uptake=[0.0,0.0]

	##interaction calculation
	#a=[1.0,11.0,4.7,1.0,5.4,5.4,2.4,1.0,1.1,2.5]   ### adjustment for risk factore in order from 15  to 24  { IDU has 0.0 adjustment value}
	#a=[1.0,11.0,4.7,1.0,12,12,2.4,1.0,1.7,2.5]
	a=[1.0,mcmcTBE,4.7,1.0,mcmcTBH,mcmcTBH,2.4,1.0,mcmcTBD,2.5]
	#### ??????? Chaing diabetes to 1.7 instead of 1.1 later as alex has done manually
	####
	#if ci > 48:
	TPadjustlist=[] #[0]*len(b[0])
	for i in b[0]:
		#RPval=.002 *  math.exp(-.074 * (P[i][12] - 1))

		RPval=mcmcR *  math.exp(-1 * mcmcL * (P[i][12] - 1))

		TPadjustlist.append(RPval)
	# else: # no mcmcR
	# 		TPadjustlist=[6.08536966506534e-05]*len(b[0])

	# TPadjustlist=[0]*len(b[0])
	#TPadjustlist=[6.08536966506534e-05]*len(b[0])
	counter=-1

	Fast_RP=sum(TPadjustlist)
	#print "------ Recent transmission ", sum(TPadjustlist)

	#begintime=time.time()
	for i in b[0]:  ####CPU
		counter=counter+1
		d=P[i][15:25]
		c=np.dot(a,d)
		if c >0 :
			TPadjustlist[counter]=TPadjustlist[counter]*c


	S_matrix[b[0],0]=Tpos[0] ## first element is uptake value for test
	S_matrix[b[0],1]=Tpos[1]
	S_matrix[b[0],2]=2
	S_matrix[b[0],3]=63

	TP_matrix[b[0],0]=Uptake[0] ## first element is uptake value for test
	TP_matrix[b[0],1]=Uptake[1]
	TP_matrix[b[0],2]=0.9999391463
	TP_matrix[b[0],3]=TPadjustlist

	#print "TP adjust", TPadjustlist, np.mean(TPadjustlist)


	####@@@@ state 3 goes to 1,3,63,test
	#a=[1.0,11.0,4.7,1.0,5.4,5.4,2.4,1.0,1.7,2.5]
	#a=[1.0,11.0,4.7,1.0,12,12,2.4,1.0,1.7,2.5]
	#a=[1.0,11.0,4.7,1.0,mcmcTBH,mcmcTBH,2.4,1.0,mcmcTBD,mcmcTBS]
	a=[1.0,mcmcTBE,4.7,1.0,mcmcTBH,mcmcTBH,2.4,1.0,mcmcTBD,2.5]
	b=np.where(np.logical_and(P[:,8]==3, P[:,27] ==1)) ### state=3
	Tpos=[0,0]
	Uptake=[0.0,0.0]


	#### for 36 months 7.663588646789006e-05
	#TPadjustlist=[7.663588646789006e-05]*len(b[0])  after 3 years by R0=.0011 after 2010 it gives a great match
	#TPadjustlist=[0.00005733449]*len(b[0])
	#TPadjustlist=[6.08536966506534e-05]*len(b[0])
	#TPadjustlist=[mcmcSL]*len(b[0])


	#if ci >= 48:
	TPadjustlist=[]
	for i in b[0]:
		#Padjustlist.append(.0011 *  math.exp(-.074 * (P[i][12] - 1)))
		if P[i][12] > 120:
			TPadjustlist.append(mcmcR *  math.exp(-1 * mcmcL * (120 - 1)))  # for biger than 10 years we stablize at 5 years
		else:
			TPadjustlist.append(mcmcR  *  math.exp(-1 * mcmcL * (P[i][12] - 1)))

	# else:  # no mcmc
	#TPadjustlist=[6.08536966506534e-05]*len(b[0])


	#TPadjustlist=[6.08536966506534e-05]*len(b[0])
	counter=-1


	begintime=time.time()
	for i in b[0]:
		counter=counter+1
		d=P[i][15:25]
		c=np.dot(a,d)
		if c > 0:
			TPadjustlist[counter]=TPadjustlist[counter]*c


	S_matrix[b[0],0]=Tpos[0] ## first element is uptake value for test
	S_matrix[b[0],1]=Tpos[1]
	S_matrix[b[0],2]=1
	S_matrix[b[0],3]=3
	S_matrix[b[0],4]=63

	TP_matrix[b[0],0]=Uptake[0] ## first element is uptake value for test
	TP_matrix[b[0],1]=Uptake[1]
	# TP_matrix[b[0],0]=tp3 ## first element is uptake value for test
	# TP_matrix[b[0],1]=tp3
	TP_matrix[b[0],2]=0.00168214255273957
	TP_matrix[b[0],3]=0.99825700375
	TP_matrix[b[0],4]=TPadjustlist


	#print "-------- Rest of RP ", sum(TPadjustlist)

	###########base-case TEST
	tt1=0
	tt2=0
	ltbi_slow=0
	ltbi_fast=0
	#
	Uptake=MonthlyUptake
	Tneg=test_choice_neg
	Tpos=test_choice_pos



	### alive, in states less than 4, not tested in last 12 month
	alive=np.where(P[:,27]==1)
	#### for test
	h01=np.where(np.logical_and(P[:,27]==1,P[:,37]==1)) ### alive, maybe
	#print "number of HCW", len(h01[0]), len(alive[0]), 0.047*len(alive[0])

	if ci < 12:
		testperiod=ci
		#b01=np.where(np.logical_and(P[:,27]==1,P[:,8]<4)) ### alive, maybe
		b01=np.where(P[:,27]==1) ### alive, maybe
		b02=np.where(np.logical_and(P[:,37]==1, P[:,36]== testperiod)) ### not tested

		b1=np.intersect1d(b01,b02)
		#print "12 number of HCW not tested in last 12 months",   len(b1), ci


	elif ci>12 and ci<24:
		testperiod = ci - 12
	#print "---- ", testperiod, alive[0], P[alive[0],8], P[alive[0],36]
		#b01=np.where(np.logical_and(P[:,27]==1,P[:,8]<4)) ### alive, maybe
		b01=np.where(P[:,27]==1) ### alive, maybe
		b02=np.where(np.logical_and(P[:,37]==1, P[:,36]== testperiod)) ### HCW and not testd in last 12 months

		b1=np.intersect1d(b01,b02)
		#print "12-24 number of HCW not tested in last 12 months",   len(b1), ci



	else:
		testperiod = ci - 12
	#print "---- ", testperiod, alive[0], P[alive[0],8], P[alive[0],36]
		#b01=np.where(np.logical_and(P[:,27]==1,P[:,8]<4)) ### alive, maybe
		b01=np.where(P[:,27]==1) ### alive, maybe
		b02=np.where(np.logical_and(P[:,37]==1, P[:,36]== testperiod)) ### HCW and not testd in last 12 months

		b03=np.intersect1d(b01,b02)

		## new HCW , distributed in 12 months
		newtestperios=ci%12
		b04=np.where(np.logical_and(P[:,37]==1, P[:,36]==newtestperios))

		b1=np.concatenate((b04[0],b03),axis=0)
		#print " 24 number of HCW not tested in last 12 months", len(b03),len(b04[0]),  len(b1), ci, newtestperios



	piv=b1
	#print "number of HCW not tested in last 12 months", len(b03),len(b04[0]),  len(piv), ci
	### testing all CHW not tested in last 12 months
	for i in piv:
		if P[i,8]== 1:
			S_matrix[i,0]=visaTneg
			TP_matrix[i,0]=1
		elif  P[i,8]== 2:
			S_matrix[i,0]=visaTpos
			TP_matrix[i,0]=1
			ltbi_fast=ltbi_fast+1
		elif  P[i,8]== 3:
			S_matrix[i,0]=visaTpos
			TP_matrix[i,0]=1
			ltbi_slow=ltbi_slow+1
		else:   ### stay in current state
			S_matrix[i,0]=P[i,8]
			TP_matrix[i,0]=1


	P[piv,28]=1 	## TESTED
	P[piv,36]=ci     ### month of test
	tt1= len(piv)


	#print "teste ", len(b1)
	#print "Chosen for test , last testing cycle" , b1[0]
	####CHOOSE PEOPLE THAT HAVE NOT BEEN TESTED IN LAST YEAR BESIDE ABOVE CONDITION




	####ALIVE - LPR CASES

	#print "---- ", testperiod, alive[0], P[alive[0],8], P[alive[0],36]
	b01=np.where(np.logical_and(P[:,27]==1,P[:,8]<4)) ### alive, maybe
	#b01=np.where(P[:,27]==1) ### alive, maybe
	#testperiod= ci-12
	b02=np.where(np.logical_and(P[:,37]==0, P[:,36]<= testperiod)) ### NOT HCW and not testd in last 12 months

	b1=np.intersect1d(b01,b02)
	#print "----- ",ci, testperiod, len(b1), len(b01), len(b02)

	nn0= round(Uptake[0]  * len(alive[0]))  ### test .004 or alive population but choose from non tested before
	nn=nn0- LPRtested #### subtract the number of people turn to LPr meaning have tested this month
	#piv=np.random.choice(b1[0], nn)
	piv=np.random.choice(b1, nn)
	#print "number of NOT HCW not tested in last 12 months", len(piv), ci

	S_matrix[piv,:]=0
	TP_matrix[piv,:]=0

	for i in piv:
		if P[i,8]== 1:
			S_matrix[i,0]=visaTneg
			TP_matrix[i,0]=1
		elif  P[i,8]== 2:
			S_matrix[i,0]=visaTpos
			TP_matrix[i,0]=1
			#ltbi_fast=ltbi_fast+1
		elif  P[i,8]== 3:
			S_matrix[i,0]=visaTpos
			TP_matrix[i,0]=1
			#ltbi_slow=ltbi_slow+1




	P[piv,28]=1 	## TESTED
	P[piv,36]=ci    ### month of test
	tt2= len(piv)

	#Ntested=tt1+tt2
	#Ntested=tt1+tt2
	Ntested=tt1+tt2


	######@@@@@@ Treatment
	pp=np.where(P[:,27]==1)
	pi1=np.where(np.logical_and(P[:,8] >=4, P[:,8]  <=13))
	pi=np.intersect1d(pi1[0],pp[0])
	if len(pi) > 0:
		S_matrix, TP_matrix=Treatment(pi,P,Intervention,Treatment_matrix,S_matrix, TP_matrix,treatment_choice_pos,treatment_choice_neg)


	######@@@@@@ rest of states 14-71
	b2=np.where(P[:,27]==1)
	b1=np.where(np.logical_and(P[:,8] >=14, P[:,8]  <=71))
	b=np.intersect1d(b2[0],b1[0])


	if len(b) > 0:
		for i in b:
			temparr=np.where(STP_matrix[:,0] == P[i][8])
			#print len(temparr[0])
			if len(temparr[0]) >0:
				SS=STP_matrix[temparr[0][0]][1]  #### S to S
				TT=STP_matrix[temparr[0][0]][2]  ### T to T

				S_matrix[i][0:len(SS)]=SS  #### S to S
				TP_matrix[i][0:len(TT)]=TT  ### T to T




	##### caling activation at the end
	S_matrix, TP_matrix=Activation(P,S_matrix, TP_matrix,mcmcR,mcmcL,ci)

	S_matrix, TP_matrix=adjust_RiskOfProgression(ci,P, S_matrix, TP_matrix)

	###Normalizing
	row_sums = TP_matrix.sum(axis=1)
	TP_matrix = TP_matrix / row_sums[:, np.newaxis]
	#print "-----------", S_matrix, TP_matrix
	#print "Normalizing ", TP_matrix


	for i in xrange(len(TP_matrix)):  ### maybe parallel
		sortinds=TP_matrix[i].argsort()  ## sorting T list and then sort S based on the sorted indices
		TP_matrix[i]=TP_matrix[i][sortinds]
		S_matrix[i]=S_matrix[i][sortinds]



	#print "------", ci, Ntested, ltbi_slow, ltbi_fast
	return S_matrix, TP_matrix, RiskAverage, Ntested,  Fast_RP, tt1


def adjust_RiskOfProgression(ci,P, S_matrix, TP_matrix):
	####@@@@@ Ignored efficacy calculation for now, maybe add it later, since Alex doesn't have that it might not change a lot

	pp=np.where(P[:,27]==1) ## only alive people
	RPi1=np.where(np.logical_and((P[:,8] >=2) ,(P[:,8] <=8)))
	RPi2=np.where(np.logical_and((P[:,8] >=14) , (P[:,8] <=39)))
	# RPi2=np.where(np.logical_and((P[:,8] >=14) , (P[:,8] <=29)))
	# RPi22=np.where(np.logical_and((P[:,8] >=31) , (P[:,8] <=39)))
	RPi3=np.where(P[:,8]==62)


	RPi4=np.concatenate((RPi1[0],RPi2[0],RPi3[0]),axis=0)

	RPi=np.intersect1d(RPi4,pp[0])

	#print "RP ", len(RPi)

	#P[RPi,12]=P[RPi,12]+1
	######@@@@ maybe better or faster to get all ST_matrix of given index in temporary array and do the rest of thing
	for mi in RPi:

		S= S_matrix[mi]
		T= TP_matrix[mi]

		#if P[mi, 8] > 3:  ### for fast and slow latent is been adjusted by risk factors too
		if 63 in S:
			indx=np.where(S==63)
			sindx=indx[0][0]
			Rval=T[sindx]
			j=mi


			#######Rval=Rval * (1.486608 - (0.0031262*ci)) # new


			if P[j][8] == 23:
				#tt=Variables["Efficacy of 9H"]
				#tt=0.92
				#Rval=float(Rval * (1-tt))
				Rval=float(Rval * 0.08)

			if P[j][8]  == 30:
				#tt=Variables["Efficacy of 6H"]
				#tt=.69
				#Rval=float(Rval * (1-tt))
				Rval=float(Rval * 0.31)
				#Rval=float(Rval * 0.08)

			if P[j][8] == 39:
				#tt=Variables["Efficacy of 3HP"]
				#tt=0.92

				#Rval=float(Rval * (1-tt))
				Rval=float(Rval * 0.08)



			TP_matrix[mi,sindx]=Rval




	return  S_matrix, TP_matrix



def Activation(P,S_matrix, TP_matrix,mcmcR,mcmcL, ci):
	# pp=np.where(P[:,27]==1)
	# #pi1=np.where(np.logical_and(P[:,12] < 36, P[:,12] != 0)) ###?????MAybe need to 60
	# pi1=np.where(np.logical_and(P[:,12] < 48, P[:,12] != 0))
	# pi2=np.where(np.logical_or(P[:,8] <= 61, P[:,8] >=72))
	# pi3=np.intersect1d(pi1[0],pi2[0])
	# pi=np.intersect1d(pi3,pp)


	RiskOfProgression=0.0

	pp=np.where(P[:,27]==1) ## only alive people
	# RPi0=np.where(np.logical_and(P[:,12] <= 36, P[:,12] != 0))
	# RPi1=np.where(np.logical_and((P[:,8] >2) ,(P[:,8] <=8)))
	### counting all those in test and treatment excep in fast and slow latent since they have already been calculated
	RPi0=np.where(np.logical_and(P[:,12] <120, P[:,12] != 0))
	RPi1=np.where(np.logical_and((P[:,8] >3) ,(P[:,8] <=8)))
	#RPi2=np.where(np.logical_and((P[:,8] >=14) , (P[:,8] <39)))

	RPi2=np.where(np.logical_and((P[:,8] >=14) , (P[:,8] <=29)))
	RPi22=np.where(np.logical_and((P[:,8] >=31) , (P[:,8] <39)))
	RPi3=np.where(P[:,8]==62)


	RPi41=np.concatenate((RPi2[0],RPi1[0]),axis=0)
	RPi42=np.concatenate((RPi22[0],RPi41),axis=0)
	RPi43=np.concatenate((RPi42,RPi3[0]),axis=0)
	RPi4=np.intersect1d(RPi43,RPi0[0])


	pi=np.intersect1d(RPi4,pp[0])

	#print "Activation ", len(pi)





 	#print "Activation ", len(pi)
	if len(pi) >0:
		for i in pi:


			Tarr=S_matrix[i] ### the state probability array
			sindx=np.where(Tarr == 63) ###63: active untreated
			if len(sindx[0]) > 0: ### it exist
				#print "Activatio ", len(sindx[0])
				#print "=====", i,  P[i][12]
				# if ci < 48:
				# 	TP_matrix[i][sindx[0]]=TP_matrix[i][sindx[0]]*13.305108
				# 	#RPval=.0011 *  math.exp(-.074 * (P[i][12] - 1))
				# else:
				TP_matrix[i][sindx[0]]= (mcmcR  *  math.exp(-1 * mcmcL * (P[i][12] - 1)))
				#TP_matrix[i][sindx[0]]=TP_matrix[i][sindx[0]]*13.305108  # RPval # Fast latent progression/slow latent progression from Variables table

	return S_matrix, TP_matrix

def Treatment(pi,P,Intervention,Treatment_matrix,S_matrix,TP_matrix, treatment_choice_pos,treatment_choice_neg):

	b=np.zeros(4)
	a=np.zeros(4)


	#### SInce all treatments are the same I chose the first element
	Treatpos=treatment_choice_pos[0]
	Treatneg=treatment_choice_neg[0]



	# intv_id=1
	# Treatpos=int(Intervention[intv_id].treatment_choice_pos)
	# Treatneg=int(Intervention[intv_id].treatment_choice_neg)
	for i in pi: ### i is index of person id


		a[0]=P[i][7] #US
		a[1]=1-P[i][7] #FB
		a[2]=P[i][19] #HIV
		a[3]=P[i][16] ##ESRD

		#matrixrow= P[i][8] - 4  ### state -4 ar ethe matrix indices
		if P[i][8] in (4,5,6):
			matrixrow= P[i][8] - 4

		else :
			matrixrow= P[i][8] - 6  ### state -6 ar ethe matrix indices : 9 -> 3, ...
		b=Treatment_matrix[matrixrow]   ### the sensitivity or specificit values
		c=np.dot(a,b)


		if P[i][8] == 4 or P[i][8] == 9:
			porval=0.76 ### can be read from varivale table
		else:
			porval=0.83

		Trueval=c * porval




		if P[i][8] in (4,5,6,7,8) : #### infected testing
			S=(P[i][14][-2], Treatpos)    #### ### pi.statelist[-2] : second last item , 2 or 3
			TP=(1-Trueval,Trueval)

		if P[i][8] in (9,10,11,12,13):
			S=[1, Treatneg]
			TP=[1-Trueval,Trueval]


		####@@@@ S_matrix and TP_matrix have 4 columns filled by zero and now only 2 column get value thatw why I gdo it in thi sway
		S_matrix[i][0:2]=S
		TP_matrix[i][0:2]=TP


	return S_matrix, TP_matrix


def Assign_Next_Step( P, S_matrix, TP_matrix, Dead):
	RC_count=0 ## recent transmission 1->2
	InitialFL=0
	leavefast=0


	Ini_un=0
	Ini_fl=0
	Ini_sl=0
	Ini_treat=0
	Ini_act=0

	NewTEST=[]
	begintime=time.time()
	for i in xrange(P.shape[0]):
		S=S_matrix[i]
		T=TP_matrix[i]


		newstate=0


		T=np.cumsum(T) ### cumulative sum
		if sum(T) == 0 :
			print "S is empty ", i, S[i]

		r=random.uniform(0.0,1.0)
		# r_cpu=r_gpu.get()
		# r=r_cpu[i]
		#print "RRR ", type(r),r
		for j in xrange(len(T)):
			#print "assign ", r , T[j]
			if float(T[j])>float(r):
				#if ci ==1 :
					#print "****** ", j, T[j], r, S[j]
				newstate=S[j]
				break

		##NewTEST.append(newstate)

		# if newstate == 0:
		# 	print "ERROR NEW STATE IS ZERO",i , P[i][8], S_matrix[i],TP_matrix[i]

		if newstate in (2,3,30) and P[i][8] == 1:  ## from uninfected
			if newstate == 2:
				#P[i][12]= round(random.uniform(0.0,1.0) * 36) #### 3 years in FL
				P[i][12]= 1
			elif newstate == 3:
				print "KHATARRRRRRRRRRRRRRRR should be nothing"
				P[i][12]=36
			else : ## 30
				#P[i][12] = 1000
				P[i][12]=121



		if newstate in (2,3,30) and P[i][8] == 0: ## come to the model
				### using weighted random number or like as exponential
				if newstate == 2:
					# if ci==0:
					# 	rexpo=np.random.choice(3, replace=True, p=[0.1,.2,.7])
					# 	if rexpo== 0:
					# 		P[i][12]= round(random.uniform(1.0,13)) ####
					# 	elif rexpo==1:
					# 		P[i][12]= round(random.uniform(12,25)) ####
					# 	else:
					# 		P[i][12]= round(random.uniform(25,36)) ##
					# else:
					P[i][12]= round(random.uniform(0.0,1.0) * 36)
					# rexpo=np.random.choice(3, replace=True, p=[0.7,.2,.1])
					# if rexpo== 0:
					# 	P[i][12]= round(random.uniform(1.0,13)) ####
					# elif rexpo==1:
					# 	P[i][12]= round(random.uniform(12,25)) ####
					# else:
					# 	P[i][12]= round(random.uniform(25,36)) ####

				elif newstate == 3 : ## 3 or 30
					# rexpo=np.random.choice(5, replace=True, p=[.7,.2,.05,.025,.025])
					# if rexpo== 0:
					# 	P[i][12]= round(random.uniform(36,48)) ####
					# elif rexpo==1:
					# 	P[i][12]= round(random.uniform(48,60)) ####
					# elif rexpo==2:
					# 	P[i][12]= round(random.uniform(60,72)) ####
					# elif rexpo==3:
					# 	P[i][12]= round(random.uniform(72,84)) ####
					# elif rexpo==4:
					# 	P[i][12]= round(random.uniform(84,96)) ####
					r=random.uniform(0,1)
					#print "---- i35", P[i][35]
					if r < (1 - P[i][35]):  #### between 3 and 10 years
						P[i][12]= round(random.uniform(37,120))
					else:
						P[i][12]=121

				else:
					P[i][12]=121


		##### drop out treatment
		if newstate == 2  and P[i][8] in (36,37,38):
			#print "DROPOUT ", P[i][8],P[i][12]
			if P[i][12] <= 36:
				P[i][8]=2
			if 	P[i][12] > 36:
				P[i][8]=3


		#if newstate == 2:
			#print "previous state ", P[i][8]

		#### COUNT RECENT Transmission
		if newstate == 2 and P[i][8] == 1:
			RC_count=RC_count+1



		##### Just for test and count
		if newstate == 2 and P[i][8] == 0:
			InitialFL=InitialFL+1


		########## just for test
		if newstate == 2 and P[i][8] == 0:
			Ini_fl=Ini_fl+1
		if newstate == 3 and P[i][8] == 0:
			Ini_sl=Ini_sl+1
		if newstate == 1 and P[i][8] == 0:
			Ini_un=Ini_un+1
		if newstate == 30 and P[i][8] == 0:
			Ini_treat=Ini_treat+1
		if newstate == 63 and P[i][8] == 0:
			Ini_act=Ini_act+1


		if newstate > 2 and P[i][8] == 2:  ## 2 to 3 and 2 otehr states
			leavefast=leavefast + 1





		P[i][8]=newstate

		P[i][14].append(newstate)



		if P[i][8] == 72:
			P[i][27]=0
			Dead=Dead+1




	#print "Assign -- initial , transition, leavefast", InitialFL, RC_count, leavefast
	#print "----- CPU", endtime-begintime #,  NewTEST
	##### Test
	# tt=np.where(P[:,8] == 30)
	# print "Initilized to treatment ", len(tt[0])
	#
	# tt=np.where(P[:,8] == 36)
	# print "choose for treatment ", len(tt[0])


	#print "++++++++++++++++++++++ FL", InitialFL,RC_count
	total=Ini_un+Ini_fl+Ini_sl+Ini_treat+Ini_act
	###print "++++++++++Initializing numbers", total,Ini_un,Ini_fl,Ini_sl,Ini_treat,Ini_act
	incidence=Ini_fl+Ini_sl+RC_count
	#print "incidence ",  incidence

	return P, Dead, RC_count, InitialFL, leavefast


def Cal_RiskOfProgression(ci,P, S_matrix, TP_matrix,Susceptible_ActiveCase_dict):
	####@@@@@ Ignored efficacy calculation for now, maybe add it later, since Alex doesn't have that it might not change a lot
	RiskOfProgression=0.0
	FB_RiskOfProgression=0.0
	USB_RiskOfProgression=0.0
	TB_Diabetes=0
	FB_TB_Diabetes=0
	USB_TB_Diabetes=0
	TB_ESRD=0
	FB_TB_ESRD=0
	USB_TB_ESRD=0
	TB_HIV=0
	FB_TB_HIV=0
	USB_TB_HIV=0
	TB_Smoking=0
	FB_TB_Smoking=0
	USB_TB_Smoking=0
	MonthSinceInf_cumulative=[]

	pp=np.where(P[:,27]==1) ## only alive people
	RPi1=np.where(np.logical_and((P[:,8] >=2) ,(P[:,8] <=8)))
	RPi2=np.where(np.logical_and((P[:,8] >=14) , (P[:,8] <=39)))
	# RPi2=np.where(np.logical_and((P[:,8] >=14) , (P[:,8] <=29)))
	# RPi22=np.where(np.logical_and((P[:,8] >=31) , (P[:,8] <=39)))
	RPi3=np.where(P[:,8]==62)
	#RPi31=np.where(P[:,8]==63)


	#RPi4=np.concatenate((RPi1[0],RPi2[0],RPi3[0],RPi31[0]),axis=0)
	RPi4=np.concatenate((RPi1[0],RPi2[0],RPi3[0]),axis=0)

	RPi=np.intersect1d(RPi4,pp[0])
	#print "RP ", len(RPi1[0]), len(RPi2[0]), len(RPi)
	#print "++++++++++ Cal RP ", len(RPi)

	en=np.where(P[RPi,16]==1)
	dn=np.where(P[RPi,23]==1)
	smcount=0
	#P[RPi,12]=P[RPi,12]+1
	######@@@@ maybe better or faster to get all ST_matrix of given index in temporary array and do the rest of thing
	for mi in RPi:

		S= S_matrix[mi]
		T= TP_matrix[mi]

		if 63 in S:
			indx=np.where(S==63)
			sindx=indx[0][0]
			Rval=T[sindx]
			j=mi

			#print "==================== cal risk of progression ", P[mi][8], Rval



			#print Rval
			### new set up using US born/FB born instead of bp
			#Susceptible_ActiveCase_dict[str(P[j][7]),P[j][2]][1]=float(Susceptible_ActiveCase_dict[str(P[j][7]),P[j][2]][1]+Rval)
			#Susceptible_ActiveCase_dict[P[j][7],P[j][2]][1]=float(Susceptible_ActiveCase_dict[P[j][7],P[j][2]][1]+Rval)
			Susceptible_ActiveCase_dict[P[j][7],P[j][2]]=float(Susceptible_ActiveCase_dict[P[j][7],P[j][2]]+Rval)

			RiskOfProgression=RiskOfProgression+Rval




			####### FB
			if P[j][7] == 0: # FB

				FB_RiskOfProgression= FB_RiskOfProgression + Rval


			if P[j][7] == 1: # USB

				USB_RiskOfProgression= USB_RiskOfProgression + Rval



			######### Counting Active cases + risk factors
			if P[j][16] == 1: # ESRD
				smcount=smcount+1
				TB_ESRD= TB_ESRD + Rval

			if P[j][16] == 1 and P[j][7]==0: # ESRD
				smcount=smcount+1
				FB_TB_ESRD= FB_TB_ESRD + Rval

			if P[j][16] == 1 and P[j][7]==1: # ESRD
				smcount=smcount+1
				USB_TB_ESRD= USB_TB_ESRD + Rval


			if P[j][23] == 1: # Diabetes
				TB_Diabetes=TB_Diabetes + Rval
			if P[j][23] == 1 and P[j][7]==0: # Diabetes
				FB_TB_Diabetes=FB_TB_Diabetes + Rval
			if P[j][23] == 1 and P[j][7]==1: # Diabetes
				USB_TB_Diabetes=USB_TB_Diabetes + Rval


			if P[j][24] == 1: # Smoking
				TB_Smoking=TB_Smoking + Rval
			if P[j][24] == 1 and P[j][7]==0: # Diabetes
				FB_TB_Smoking=FB_TB_Smoking + Rval
			if P[j][24] == 1 and P[j][7]==1: # Diabetes
				USB_TB_Smoking=USB_TB_Smoking + Rval





			if P[j][19] == 1 or P[j][20] == 1: # HIV
				TB_HIV=TB_HIV + Rval

			if P[j][7] ==0:
				if P[j][19] == 1 or P[j][20] == 1: # HIV
					FB_TB_HIV=FB_TB_HIV + Rval

			if P[j][7] ==1:
				if P[j][19] == 1 or P[j][20] == 1: # HIV
					USB_TB_HIV=USB_TB_HIV + Rval




	#print "++++++ RP", RiskOfProgression
	#### TEST FOR RECENT TRANSMISSION: GING FROM 2 TO 63
	RT_RiskOfProgression=0
	a1=np.where(np.logical_and((P[:,12] < 36) ,(P[:,27] ==1)))
	for mi in a1[0]:

		S= S_matrix[mi]
		T= TP_matrix[mi]

		if 63 in S:
			indx=np.where(S==63)
			sindx=indx[0][0]
			Rval=T[sindx]


			RT_RiskOfProgression=RT_RiskOfProgression+Rval



	#ac=np.where(np.logical_and((P[:,27] ==1) ,(P[:,8] ==63)))
	#RiskOfProgression=RiskOfProgression+len(ac[0])
	#print "=========== RISK OF PROGRESSION ",  RiskOfProgression, sum(Susceptible_ActiveCase_dict.values())
	#print " RP,  Diabetes, ESRD, HIV ", len(RPi),len(en[0]), smcount, RiskOfProgression, TB_ESRD, TB_Diabetes, TB_HIV

	return RiskOfProgression,Susceptible_ActiveCase_dict,RT_RiskOfProgression, TB_Diabetes, FB_TB_Diabetes,USB_TB_Diabetes,TB_ESRD, FB_TB_ESRD,USB_TB_ESRD,TB_HIV,FB_TB_HIV,USB_TB_HIV, TB_Smoking,FB_TB_Smoking,USB_TB_Smoking, FB_RiskOfProgression, USB_RiskOfProgression

def Update_Cycle(P,ci,LifeDeath_Stratum_dict,InteractionAdjustDitc,Age_Group_Dict, Dead):

	Riskfactor_id=[78,83,87,91,179,183,184,194,189,74,163,164,165,166,167,168,169,170,171,172]
	Riskfactor_name=['Homeless','ESRD','TNF_alpha','Alcohol','Diabetes','HIV','HIV_ART','Transplant','IDU','Smoker','Age 35-39','Age 40-44','Age 45-49','Age 50-54','Age 55-59','Age 60-64','Age 65-69','Age 70-74','Age 75-79','Age 80+']

	riskfactor_idname_dict={'Smoker':24,'Homeless':15,'ESRD':16,'TNF_alpha':17,'Alcohol':18,'Diabetes':23,'HIV':19,'HIV_ART':20,'IDU':22,'Transplant':21}

	cycle_duration=1 ### maybe change later and be input argument

	b=np.where(np.logical_and(P[:,23]==0,P[:,27]==1))  ### no diabeties
	randarr= np.random.uniform(0.0,1.0,len(b[0]))
	indx=np.where( randarr <  0.000622191 )
	P[indx[0],23]=1
	P[indx[0],26]=1


	###HIV
	b=np.where(np.logical_and(P[:,19]==0,P[:,27]==1))  ### no HIV
	randarr= np.random.uniform(0.0,1.0,len(b[0]))
	indx=np.where( randarr <  2.42358e-05 )
	P[indx[0],19]=1
	P[indx[0],26]=1

	### Transplant
	b=np.where(np.logical_and(P[:,21]==0,P[:,27]==1))
	randarr= np.random.uniform(0.0,1.0,len(b[0]))
	indx=np.where( randarr <  5.3025e-06)
	P[indx[0],21]=1
	P[indx[0],26]=1


	#### No Smoking to  smoking
	b=np.where(np.logical_and(P[:,24]==0,P[:,27]==1))
	randarr= np.random.uniform(0.0,1.0,len(b[0]))
	indx=np.where( randarr <  0.0001333333 )
	P[indx[0],24]=1
	P[indx[0],26]=1

	### Smoking to no smoking
	b=np.where(np.logical_and(P[:,24]==1,P[:,27]==1))
	randarr= np.random.uniform(0.0,1.0,len(b[0]))
	indx=np.where( randarr <  0.004309472 *10) ### 10 is added for calibration
	P[indx[0],24]=0
	P[indx[0],26]=1

	#### No ESRD to ESRD ( adjustment for having Diabetes)
	pi1=np.where(P[:,27]==1)
	pi2=np.where(np.logical_and(P[:,16]==0,P[:,24]==1)) ## a
	b=np.intersect1d(pi1[0],pi2[0])


	if len(b) >0 :
		randarr= np.random.uniform(0.0,1.0,len(b))
		indx=np.where( randarr <  5 * 8.9802e-06 )    #####??? 10.4 to 7
		P[indx[0],16]=1
		P[indx[0],26]=1

	### no diabeities
	pi2=np.where(np.logical_and(P[:,16]==0,P[:,24]==0)) ## and having diabeties
	b=np.intersect1d(pi1[0],pi2[0])

	if len(b) >0 :
		randarr= np.random.uniform(0.0,1.0,len(b))
		indx=np.where( randarr <  8.9802e-06 )
		P[indx[0],16]=1
		P[indx[0],26]=1

			####TNF alpha  #### adjustment for different age groups
	b=np.where(np.logical_and(P[:,17]==0,P[:,27]==1))  ### no diabeties
	adjval=[4.16091954,4.16091954,5.16091954,5.16091954,7.275862069,7.275862069,10.27586207,10.27586207,7.988505747,6.149425287]
	for i in b[0]:


		if (P[i][10] >= 35*12 and P[i][10] < 39*12):
			tpadj= 8.9802e-06 * adjval[0]
		elif  (P[i][10] >= 40*12 and P[i][10] < 44*12):
			tpadj= 8.9802e-06 * adjval[1]
		elif  (P[i][10] >= 45*12 and P[i][10] < 49*12):
			tpadj= 8.9802e-06 * adjval[2]
		elif  (P[i][10] >= 50*12 and P[i][10] < 54*12):
			tpadj= 8.9802e-06 * adjval[3]
		elif (P[i][10] >= 55*12 and P[i][10] < 59*12):
			tpadj= 8.9802e-06 * adjval[4]
		elif  (P[i][10] >= 60*12 and P[i][10] < 64*12):
			tpadj= 8.9802e-06 * adjval[5]
		elif (P[i][10] >= 65*12 and P[i][10] < 69*12):
			tpadj= 8.9802e-06 * adjval[6]
		elif  (P[i][10] >= 70*12 and P[i][10] < 74*12):
			tpadj= 8.9802e-06 * adjval[7]
		elif  (P[i][10] >= 75*12 and P[i][10] < 80*12):
			tpadj= 8.9802e-06 * adjval[8]
		elif (P[i][10] >= 80*12):
			tpadj= 8.9802e-06 * adjval[9]
		else:
			tpadj= 8.9802e-06



		randarr= np.random.uniform(0.0,1.0)
		if  randarr <  tpadj :
			P[indx[0],17]=1
			P[indx[0],26]=1


	P[:,10]=P[:,10] + 1  ### age as month
	P[:,11]=P[:,11] + 1  #### Cycle
	P[:,12]=P[:,12] + 1   #### Months since infection
	#P[:,31]=P[:,31] + 1  ###years in US


	for i in xrange(len(P)):
		if P[i][10] in Age_Group_Dict.keys():
	 		 P[i][3] =  Age_Group_Dict[P[i][10]]

	b=np.where(P[:,27]==1)
	# mykeys=zip(P[b[0],1],P[b[0],3])
	# tpbase=np.asarray([LifeDeath_Stratum_dict[x] for x in mykeys])
	tpbase=np.zeros(len(b[0]))
	counter=-1
	for i in b[0]:
		counter=counter+1
		stratname=str(P[i][1]) + ' ' + str(P[i][3])  ### only has sex and age group as stratum name
	 	tpbase[counter]=float(LifeDeath_Stratum_dict[stratname]) ### get the risk value
		#print "=== ", i, stratname, tpbase[counter]



	#print " Life to death tpbase", tpbase
	a=P[b[0],15:25]  ### risk factors
	d=[1.0,5.9,1.41,1.0,5.6,1.24,15.0,1.0,3.0,1.8]
	adjustval=a.dot(d)
	adjustval[adjustval == 0] = 1.0
	# print " Life to death adjustval ", type(tpbase),type(adjustval)
	tpbase2=tpbase * adjustval
	# print " Life to death tpbase ",
	randarr= np.random.uniform(0.0,1.0,len(b[0]))


	comparearr=np.greater(tpbase2,randarr)
	c=np.where(comparearr== True)
	P[c[0],27]=0
	Dead=Dead+len(c[0])
	# print " Life to death Dead ", Dead


	####### GOING FROM FL TO SLOWLATENT AFTER 36 months


	a1=np.where(np.logical_and(P[:,8]==2,P[:,12]==36)) ###
	#a1=np.where(np.logical_and(P[:,8]==2,P[:,12]==48))
	#print "FL to SL", len(a1[0]), a1[0]
	if len(a1[0]) > 0:
		P[a1[0],8]=3
		#print "FL to SL", len(a1[0])
		#P[a1[0],12]= 1000
		#P[a1[0],8]=3

	return P, Dead


##@package Active_Case_Finding
#@param pi person class object
#@brief  This function based on the number of active cases in population choose people in slow latent or fast latent state randomly for test
def Active_Case_Finding(P,ci, ActivacaseRP,   Intervention):

	total_fast_latents_identified=0.0
	total_slow_latents_identified=0.0
	flag=0
	r=0.0
	chance_fast_latent=0.0
	chance_slow_latent=0.0

	FLi=np.where(P[:,8] ==2)
	#if pi[8] == 2: ### fast latent
	for i in FLi[0]:

		number_of_fast_latents_identified_per_active_case = 10.0 * 0.25 * 0.75
		number_of_active_cases_last_cycle = ActivacaseRP[ci-1]  ## count sum of risk of progression as active case


		total_fast_latents_identified = number_of_fast_latents_identified_per_active_case * number_of_active_cases_last_cycle
		#if FastLatent_number[ci-1] > 0:
		if len(FLi[0]) > 0:
			chance_fast_latent = total_fast_latents_identified / len(FLi[0])

			r=float(random.uniform(0.0,1.0))

			if r < chance_fast_latent:
				#print "active case finindg fast latent"

				# P[i][13]=1 ## choose this person for test
				# intv_id=P[i][13]
				Tpos=Intervention[1].test_choice_pos  ### by default choose test #1
				Tpos=Tpos.strip()

				# SS=States[Tpos]
				# print "test ", Tpos, SS,int(SS)
				P[i][8]=int(Tpos)
				#P[i][14][ci]=SS
				P[i][14].append(int(Tpos))
				P[i][36]=ci
				P[i][28]=1 ###### @@@@@ check that this not going to nextstep assign where th tested is set there too



	SLi=np.where(P[:,8] ==3)
	for i in SLi[0]:

		number_of_slow_latents_identified_per_active_case = 10.0 * 0.25 * 0.25
		number_of_active_cases_last_cycle = ActivacaseRP[ci-1]

		total_slow_latents_identified = number_of_slow_latents_identified_per_active_case * number_of_active_cases_last_cycle
		#if SlowLatent_number[ci-1] > 0:

		#chance_slow_latent = float(total_slow_latents_identified / SlowLatent_number[ci-1])
		chance_slow_latent = float(total_slow_latents_identified / len(SLi[0]))


		r = float(random.uniform(0.0,1.0))

		if r < chance_slow_latent:

			Tpos=Intervention[1].test_choice_pos ### by default choose test number 1
			Tpos=Tpos.strip()

			P[i][8]=int(Tpos)

			P[i][14].append(int(Tpos))
			P[i][36]=ci
			P[i][28]=1
	return P


# def first_cycle(P,TP_dict_ltbi):
# 	#### ALL people going from 0 to (1,2,3,30) are only stratified and the stratified id =1
#
# 	S_matrix=np.zeros((len(P),5), dtype='float64')
# 	TP_matrix=np.zeros((len(P),5), dtype='float64')
#
# 	for i in xrange(len(P)):
# 		S=[]
# 		TProb=[]
# 		S.append(0)
# 		TProb.append(0.0)
# 		for j in (1,2,3,30): #### from 0 it only goes to these states
#
#
# 			#### staratum id =1 (lengthin us+_bp+sex+race+age group)
# 			stratname= str(P[i][5]) +  ' ' + str(P[i][6]) + ' '  + str(P[i][1]) +  ' ' + str(P[i][2]) +  ' ' + str(P[i][3])
# 			#print "First cycle ", i, P[i][8], j, stratname
# 			tpval=TP_dict_ltbi[P[i][8],j][stratname]###get tp value by stratum name
# 			S.append(j)  ### add the next state and corresponding tp value in to list to be use later
# 			TProb.append(tpval)
#
# 		S_matrix[i]=S
# 		TP_matrix[i]=TProb
#
# 	row_sums = TP_matrix.sum(axis=1)
# 	TP_matrix = TP_matrix / row_sums[:, np.newaxis]
#
#
#
# 	for i in xrange(len(TP_matrix)):  ### maybe parallel
# 		sortinds=TP_matrix[i].argsort()  ## sorting T list and then sort S based on the sorted indices
# 		TP_matrix[i]=TP_matrix[i][sortinds]
# 		S_matrix[i]=S_matrix[i][sortinds]
#
#
#
# 	return S_matrix, TP_matrix

def first_cycle_LTBI(P,TP_dict,ci):
	#### ALL people going from 0 to (1,2,3,30) are only stratified and the stratified id =1

	S_matrix=np.zeros((len(P),5), dtype='float64')
	TP_matrix=np.zeros((len(P),5), dtype='float64')


	for i in xrange(len(P)):
		S=[]
		TProb=[]
		#S.append(0)
		#TProb.append(0.0)
		for j in (1,2,3,30,63): #### from 0 it only goes to these states
		#for j in (1,3,30,63): #### from 0 it only goes to these states
			#print j
			#### staratum id =1 (lengthin us+_bp+sex+race+age group)
			#tpval=0
			stratname= str(P[i][5]) +  ' ' + str(P[i][6]) + ' '  + str(P[i][1]) +  ' ' + str(P[i][2]) +  ' ' + str(P[i][3])

			#tpval=TP_dict[P[i][8],j][stratname]###get tp value by stratum name
			#print "Stratum name", stratname,
			tpval=TP_dict[0,j][stratname]###get tp value by stratum name
			S.append(j)  ### add the next state and corresponding tp value in to list to be use later
			TProb.append(tpval)
		#print "First cycle ", i, P[i][8],  stratname, j,TProb

		#print "---", S
		S_matrix[i]=S
		TP_matrix[i]=TProb




	#sstt='5 or more years Nicaragua Female Black Age 65-69'
	#print '--------------',TP_dict[0,1][sstt],TP_dict[0,2][sstt],TP_dict[0,3][sstt]
	if ci >1:

		#### UPDATING LTBI PREVELANCE afte cycle 2
		#b1=np.where(P[:,7] == 0) ### FB
		b1=np.where(P[:,27] == 1) ### alive
		#print "----new commers size", len(P)
		#for i in b1[0]:
		for i in range(len(P)):
			##print "--------------- before ",TP_matrix[i,:]
			#print "Decrease", P[i][31],P[i][32],P[i][33]
			tmp1= TP_matrix[i,2]    ### Slow LAtent
			tmp2=P[i][31]
			tmp3= tmp1 * (math.pow(tmp2,ci))
			#print "++++++++++++", tmp1,tmp2,tmp3
			TP_matrix[i,2] = tmp3


			tmp1= TP_matrix[i,3]    ### treated
			tmp2=P[i][31]
			tmp3= tmp1 *(math.pow(tmp2,ci))
			TP_matrix[i,3] = tmp3


			tmp1= TP_matrix[i,1]    ### fast latent
			tmp2=P[i][32]
			tmp3= tmp1 *(math.pow(tmp2,ci))
			TP_matrix[i,1] = tmp3


			tmp1= TP_matrix[i,4]    ### active cases
			tmp2=P[i][33]
			tmp3= tmp1 *(math.pow(tmp2,ci))
			TP_matrix[i,4] = tmp3


			#print "LTBI pval", P[i][31],P[i][32],P[i][33]
			###print "--------------- after",TP_matrix[i,:]




	#print "------ ", S_matrix, TP_matrix

	row_sums = TP_matrix.sum(axis=1)
	TP_matrix = TP_matrix / row_sums[:, np.newaxis]



	for i in xrange(len(TP_matrix)):  ### maybe parallel
		sortinds=TP_matrix[i].argsort()  ## sorting T list and then sort S based on the sorted indices
		TP_matrix[i]=TP_matrix[i][sortinds]
		S_matrix[i]=S_matrix[i][sortinds]


    #print "************************ First cycle ", S_matrix, TP_matrix
	return S_matrix, TP_matrix



def Outgoing_pop(P):

		b=np.where(P[:,27]==1)
		outgoingrate=P[b[0],29]
		randarr= np.random.uniform(0.0,1.0,len(b[0]))



		comparearr=np.greater(outgoingrate,randarr)
		c=np.where(comparearr== True)
		#print "Outgoing ", c[0], len(c[0])
		P[c[0],27]=0
		#endtime=time.time()
		#print 	"outgoing  ", endtime-begintime, len(c[0])
		return P



def Visa_Status_Leave(P):
	#####???? This way of selecting array by having P[b[0],] is not working correctly, its better to have np.logical_and
	#### but since teh conditions are already two conditions, I avoid only choose alive people,
	### so I choose maybe dead people too, but they leave again :)
	b=np.where(P[:,27]==1)
	#Monthlyrate=np.zeros(len(b[0]))
	Monthlyrate=np.zeros(len(P))

	#### m1 visa leaving after 12 months
	a1=np.where(np.logical_and(P[:,11]==13,P[:,30]==14)) ###
	Monthlyrate[a1[0]]=1
	#
	#
	#
	# a2=np.where(np.logical_and(P[b[0],11]==24,P[b[0],30]==11)) ###
	# Monthlyrate[a2[0]]= 0.26
	#
	#
	#
	# a3=np.where(np.logical_and(P[b[0],11]==96,P[b[0],30]==12)) ###
	# Monthlyrate[a3[0]]= 0.4
    #### Temporary workers
	a4=np.where(np.logical_and(P[:,11]==36,P[:,30]==9)) ###
	Monthlyrate[a4[0]]= 0.85

	a5=np.where(np.logical_and(P[:,11]==72,P[:,30]==9)) ###
	Monthlyrate[a5[0]]= 1



	a8=np.where(np.logical_and(P[:,11]==24,P[:,30]==3)) ### diplomats
	Monthlyrate[a8[0]]= 1
	### xchange workers
	a9=np.where(np.logical_and(P[:,11]==12,P[:,30]==4)) ###
	Monthlyrate[a9[0]]= .2
	a10=np.where(np.logical_and(P[:,11]==24,P[:,30]==4)) ###
	Monthlyrate[a10[0]]= .25
	a11=np.where(np.logical_and(P[:,11]==36,P[:,30]==4)) ###
	Monthlyrate[a11[0]]= .33
	a12=np.where(np.logical_and(P[:,11]==48,P[:,30]==4)) ###
	Monthlyrate[a12[0]]= .5
	a13=np.where(np.logical_and(P[:,11]==60,P[:,30]==4)) ###
	Monthlyrate[a13[0]]= 1

	#randarr= np.random.uniform(0.0,1.0,len(b[0]))
	randarr= np.random.uniform(0.0,1.0,len(P))

	comparearr=np.greater(Monthlyrate,randarr)
	c=np.where(comparearr== True)

	tp1=np.nonzero(Monthlyrate)
	#print " ++++++++++++++ Monthly leave visas", P[tp1[0],30]

	P[c[0],27]=0   ### they are leaving

	#### SOME CHANGE THEIR VISA STATUS



	return P

def Visa_Status_Change(P,ci):
	b=np.where(P[:,27]==1)
	#Monthlyrate=np.zeros(len(b[0]))
	Monthlyrate=np.zeros(len(P))
	### students to LPR, all student visas have the same pro to go to LPR
	#a1=np.where(np.logical_and(P[b[0],11]< 48,P[b[0],30]==8)) ###
    ##########
	a1=np.where(np.logical_and(P[:,27]==1,P[:,30]==14)) ###

	#print "----14", P[a1[0],30]
	Monthlyrate[a1[0]]= 0.002549585

	a1=np.where(np.logical_and(P[:,27]==1,P[:,30]==15)) ###
	#print "----15", P[a1[0],30]
	Monthlyrate[a1[0]]= 0.002549585

	a1=np.where(np.logical_and(P[:,27]==1,P[:,30]==16)) ###
	#print "----16", P[a1[0],30]
	Monthlyrate[a1[0]]= 0.002549585

	a1=np.where(np.logical_and(P[:,27]==1,P[:,30]==17)) ###
	#print "----17,", P[a1[0],30]
	Monthlyrate[a1[0]]= 0.002549585

	a1=np.where(np.logical_and(P[:,27]==1,P[:,30]==8)) ###
	#print "----8,", P[a1[0],30]
	Monthlyrate[a1[0]]= 0.002549585

	#a2=np.where(np.logical_and(P[b[0],11]<24,P[b[0],30]==11)) ###
	a2=np.where(np.logical_and(P[:,27]==1,P[:,30]==11)) ###
	#print "---- 11,", P[a2[0],30]
	Monthlyrate[a2[0]]= 0.002549585

	a3=np.where(np.logical_and(P[:,27]==1,P[:,30]==12)) ###
	#a3=np.where(P[b[0],30]==12) ###
	#a11=np.where(P[:,30]==12) ###
	#print "----12",a3,a3[0], P[a3[0],30]
#	print "---- 12,", P[a3[0],30]
	Monthlyrate[a3[0]]= 0.002549585

	###Refugees and asylees to LPR
	#a4=np.where(np.logical_and(P[b[0],11]<12,P[b[0],30]==7)) ###
	a4=np.where(np.logical_and(P[:,27]==1,P[:,30]==7)) ###
	Monthlyrate[a4[0]]= 0.032468221

	#a5=np.where(np.logical_and(P[b[0],11]<12,P[b[0],30]==1)) ###
	a5=np.where(np.logical_and(P[:,27]==1,P[:,30]==1)) ###
	Monthlyrate[a5[0]]= 0.00929342

	### AFTER ONE YEAR THEY ALL GET :LPR


	pp=np.where(P[:,27]==1)
	pi1=np.where(np.logical_and(P[b[0],11]>12,P[b[0],30]==7)) ###
	a4=np.intersect1d(pi1[0],pp[0])
	Monthlyrate[a4]= 1

	pp=np.where(P[:,27]==1)
	pi1=np.where(np.logical_and(P[b[0],11]>12,P[b[0],30]==1)) ###
	a4=np.intersect1d(pi1[0],pp[0])
	Monthlyrate[a5]= 1

	## temporary workers
	#a6=np.where(np.logical_and(P[b[0],11]< 72,P[b[0],30]==9)) ###
	a6=np.where(np.logical_and(P[:,27]==1,P[:,30]==9)) ###
	Monthlyrate[a6[0]]= 0.013504068

	## family
	a7=np.where(np.logical_and(P[:,27]==1,P[:,30]==5)) ###
	Monthlyrate[a7[0]]= 0.048304847


	tp1=np.nonzero(Monthlyrate)
	#print "???????????????visa status to LPR",tp1[0],Monthlyrate[tp1[0]], P[tp1[0],30]

	#randarr= np.random.uniform(0.0,1.0,len(b[0]))
	randarr= np.random.uniform(0.0,1.0,len(P))

	comparearr=np.greater(Monthlyrate,randarr)
	c=np.where(comparearr== True)

	#tp1=np.nonzero(Monthlyrate)
	#print " Monthly visa status change ",len(tp1[0]) ,len(c[0])


	#P[c[0],6]='Naturalized citizen'


	#### chaing the outgoing rate to similar as 'Citizen', like as othe rclasses


	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()

	for i in c[0]:
		sqlstr="select outgoing from base_init_lines_class where sex='" + str(P[i][1]) + "' and race= '" + str(P[i][2]) + "' and birthplace= '" + str(P[i][6]) + "' and class= 'Citizen'"
		#print '+++', sqlstr
		cur1.execute(sqlstr)
		row = cur1.fetchone()
		#print "sqlstr ", sqlstr, P[i][30]
		P[i][29]=row[0]

		#print "LEAVING ", P[i][29], row[0]

	P[c[0],30]=13   ### green cart status
	P[c[0],11]=1  ### new in this visa status
	P[c[0],28]=1   ### set them as tested
	P[c[0],36]=ci

	con.close()




	### number of people who turned to LPR status, they need to be set for test and their number be deducted from base-case tested
	#print "TESTED AND BEEN IN VISA STAUS CHANGE", len(h[0])   #### NNED TO BE SAVE
	h=len(c[0])

	#### CHANGE TO OTHER states
	#
	# Monthlyrate=np.zeros(len(b[0]))
	# a1=np.where(np.logical_and(P[b[0],11]> 48,P[b[0],30]==8)) ### undergrad to master
	#
	# Monthlyrate[a1[0]]= .38
	#
	# randarr= np.random.uniform(0.0,1.0,len(b[0]))
	#
	# comparearr=np.greater(Monthlyrate,randarr)
	# c=np.where(comparearr== True)
	#
	#
	# P[c[0],30]=11   ### mastet student
	# P[c[0],11]=1  ### new in this visa status
	#
	# Monthlyrate=np.zeros(len(b[0]))
	# a1=np.where(np.logical_and(P[b[0],11]> 48,P[b[0],30]==8)) ### undergrad to master
	#
	# Monthlyrate[a1[0]]= .15
	#
	# randarr= np.random.uniform(0.0,1.0,len(b[0]))
	#
	# comparearr=np.greater(Monthlyrate,randarr)
	# c=np.where(comparearr== True)
	#
	#
	# P[c[0],30]=12   ### dostoral student
	# P[c[0],11]=1  ### new in this visa status
	#
	#
	# #### MASTERTO dostoral
	# Monthlyrate=np.zeros(len(b[0]))
	# a1=np.where(np.logical_and(P[b[0],11]> 48,P[b[0],30]==11)) ### undergrad to master
	#
	# Monthlyrate[a1[0]]= .35
	#
	# randarr= np.random.uniform(0.0,1.0,len(b[0]))
	#
	# comparearr=np.greater(Monthlyrate,randarr)
	# c=np.where(comparearr== True)
	# #print "visa stats change to doctoral", len(a1[0]),len(c[0])
	# P[c[0],30]=12   ### dostoral student
	# P[c[0],11]=1  ### new in this visa status
	#

	return P, h
