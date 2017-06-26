#!/usr/bin/env python
"""
TB Modeling program
Autor: Haleh Ashki
Consultant: Alex Goodell 503 737 8361 (SMS ok)
UCSF
"""
import numpy as np
import sqlite3 as lite
import time
import random
import multiprocessing
import sys
from multiprocessing import Pool
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput



# class person():
# 	def __init__(self):
# 		self.id=0 ,0
# 		self.sex   = '',1
# 		self.race  = '',2
# 		self.age_group  = '',3
# 		self.citizen='',4
# 		self.years_in_us='',5
# 		self.birthplace='',6
# 		self.usborn=0 ,7 # default is not FB born
# 		self.state=0,8
# 		self.statename='',9
# 		self.age=0,10
# 		self.cycle=0,11
# 		self.MonthSinceTBInfection=0,12
# 		self.intervention_id=0,13
# 		self.statelist=[],14
# 		self.Homeless=0,15
# 		self.ESRD=0,16
# 		self.TNF_alpha=0,17
# 		self.Alcohol=0,18
# 		self.HIV=0  ,19 # representing HIV_noART
# 		self.HIV_ART=0,20
# 		self.Transplant=0,21
# 		self.IDU=0,22
# 		self.Diabetes=0,23
# 		self.Smoker=0,24
# 		self.agerisk=0,25
# 		self.riskfactor=0,26
# 		self.alive=1,27
# 		self.tested=0,28



class Intervention():
	def __init__(self,v1,v2,v3,v4,v5,v6,v7,v8,v9):
		self.interventionid=v1
		self.test_choice_pos=v2
		self.test_choice_neg=v3
		self.treatment_choice_pos=v4
		self.treatment_choice_neg=v5
		self.begin_cycle= v6
		self.end_cycle=v7
		self.state_names=v8
		self.monthly_testing_uptake=v9

##@package Population_Sample
#@param PopulationNumber: Number of individuals in population
#@param New  is been set if its been called for newcomers for open cohort.
#@param year  for initial step, its the year we choose to strat the program. For newcomers its the year of having newcomers.
#@return return the index and weight for each index of the base_init_lines table
#@brief this index values are used to assign the race, sex, ... for initial people
def Population_Sample( PopulationNumber, New, year):
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	cur2=con.cursor()


	if New :  ### it means newcommers and New is True

		column='weight_new_people' + str(year)
		cur1.execute('select `index`, ' + column + ' from base_init_lines')
		cur2.execute('select sum(' + column + ') from base_init_lines')
		total=cur2.fetchone()   ## sum of all weights
		total=total[0]
	else:
		cur1.execute('select `index`, weight'+str(year)+ '  from base_init_lines')
		cur2.execute('select sum(weight'+str(year)+')  from base_init_lines')
		total=cur2.fetchone()   ## sum of all weights
		total=total[0]




	elements = []
	weights = []

	for row in cur1:
		elements.append(row[0])
		if row[1] != None:  ### There is no weight for some records
			weights.append(row[1] / float(total)) ## get the percentage of weight for each index
		else:
			weights.append(0)

	A=np.random.choice(elements, PopulationNumber, p=weights)
	### A contains the index of the base_init_line table that we have to choose people from based on the weight and population size
	con.close()
	return   A

##@package Make_Base_init_dict
#@return A dictionary made based on "base_init_lines" table. The keys are the index and values are list of (sex,race,age,citizen,years_in_us,birthplace)
#@brief Making dictionary make the access faster
def Make_Base_init_dict():
	con = lite.connect('./limcat-zero-index.sqlite')

	Initial_Person_dict={}
	cur1 = con.cursor()
	cur1.execute('select `index`, sex,race,age_group,citizen,years_in_us,birthplace from base_init_lines')
	for row1 in cur1:
		dictval= [row1[1],row1[2],row1[3],row1[4],row1[5],row1[6]]
		Initial_Person_dict[row1[0]]=dictval

	con.close()
	return 	Initial_Person_dict


##@package  Make_age_group_dict
#@return a dictionary that the keys are age based on months and the values are age-groups.
#@brief  this dictionary is made because accessing the age by month as an integer is faster than using year (like 34.2) as float
def Make_age_group_dict():
	agedict={}
	# cdef int i
	# cdef int val

	for i in range(15,80,5):
		val =i+4
		agedict[int(i*12)]="Age " + str(i) + "-" + str(val)

	agedict[960]='Age 80+'
	return agedict


##@package  Make_RiskFactor_Initialization
#@return a dictionary that the keys are (riskfactor id, stratum name)  and value is tpbase from "transition_probabilities_by_stratum" table.
#@brief  this dictionary is made to have faster access to tpbase value for risk factors (uninitialized to risk factor) based  on their stratumname
def Make_RiskFactor_Initialization():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()


	RiskFactor_Stratum_dict={}
	#cur1.execute("	select transition_probabilities_by_stratum.to_state_id,  transition_probabilities_by_stratum.base,  transition_probabilities_by_stratum.stratum_name   from transition_probabilities   inner join transition_probabilities_by_stratum on  transition_probabilities.from_state_id = transition_probabilities_by_stratum.from_state_id  where  transition_probabilities_by_stratum.to_state_id >74 and transition_probabilities.from_state_name='Uninitialized' and transition_probabilities.is_stratified=1")
	#cur1.execute("select transition_probabilities_by_stratum.to_state_id,   transition_probabilities_by_stratum.base,  transition_probabilities_by_stratum.stratum_name  from transition_probabilities   inner join transition_probabilities_by_stratum on  transition_probabilities.from_state_id = transition_probabilities_by_stratum.from_state_id  where  transition_probabilities.to_state_id >74 and transition_probabilities.from_state_name='Uninitialized' and transition_probabilities.is_stratified=1 and transition_probabilities.to_state_id in (78,83,87,91,179,183,184,194,189,74)")
	#cur1.execute("select transition_probabilities_by_stratum.to_state_id,   transition_probabilities_by_stratum.base,  transition_probabilities_by_stratum.stratum_name   from transition_probabilities   inner join transition_probabilities_by_stratum on  transition_probabilities.from_state_id = transition_probabilities_by_stratum.from_state_id  where  transition_probabilities_by_stratum.to_state_id >74 and transition_probabilities.from_state_name='Uninitialized' and transition_probabilities.is_stratified=1 and transition_probabilities_by_stratum.to_state_id in (78,83,87,91,179,183,184,194,189,74)")
	cur1.execute("select  to_state_id, base,  stratum_name  from  transition_probabilities_by_stratum    where  from_state_name='Uninitialized' and  to_state_id in (78,83,87,91,179,183,184,194,189,74)")
	for row in cur1:
		RiskFactor_Stratum_dict[row[0],row[2]] = float(row[1])

	con.close()
	return RiskFactor_Stratum_dict




##@package Make_RiskFactor_StratumType_dict
#@return a dictionary that the keys are to_state_id  and value is stratum_type_id
#@brief  The keys are those risk factors that been considered initially this program( not all been used though).
#Smoker,Homeless,ESRD,TNF-alpha,Alcohol,Diabetes,Infected HIV, no ART,Infected HIV, ART,IDU,Transplant patient
def Make_RiskFactor_StratumType_dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	RF_Stratum={}
	cur1.execute("select to_state_id,  stratum_type_id from transition_probabilities where to_state_id in (78,83,87,91,179,183,184,194,189,74)  and is_stratified=1 and from_state_name='Uninitialized' ")

	for row in cur1:
		RF_Stratum[row[0]]=int(row[1])

	con.close()
	return RF_Stratum

##@package Make_LifetoDeath_baseval_dict
#@return a dictionary that the keys are stratum name and value is tpbase, the transition probability of going from live to death
#@brief  This dictionary contain the transition peobabity of going from live to death for different stratum names.
def Make_LifetoDeath_baseval_dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	LifetoDeath_Stratum={}
	cur1.execute("select stratum_name, base from transition_probabilities_by_stratum where from_state_id=175 and to_state_id=176  ")
	for row in cur1:
		LifetoDeath_Stratum[str(row[0].strip())]=float(row[1])

	con.close()
	return LifetoDeath_Stratum


##@package Make_monthly_RiskFactor_chance_dict
#@return a dictionary that the keys are to_state_id which are the risk factors, and values are the transition probability
#@brief  This dictionary contain the monthly transition probability of going from not having risk factors to have risk factors, for example from no-hiv to hiv
def Make_monthly_RiskFactor_chance_dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	MonthRF_hash={}
	MonthRF_hash={}
	cur1.execute("select to_state_id, tp_base from transition_probabilities where  substr(description,1,7) = 'Monthly' and from_state_id >=74 and to_state_id in (78,83,87,91,179,183,184,194,189,74)" )
	for row1 in cur1:
		MonthRF_hash[row1[0]]=float(row1[1])

	con.close()
	return MonthRF_hash

##@package Make_TransitionProb_FromTo_Dict
#@return two dictionaries. 1: TP: keys: combination of (from_state, to_state), values : are dictionaries too. Keys are stratum name and values are tpbase.
#2:from_to_state_dict : keys : from_state_id , vakues: list of tpbase, is_startified, stratum_type_id
#@brief  The first 75 states are the TB chain states. And in order to cut the values are not used here, only those states are obtaind from the table
#the from_to_state_dict is used when TP is not stratified and the tpbase comes from "transition_probability" table
#the TP dictionary is used to get the tpbase for transitions that are stratified and so the tpbase is based on the stratumname
#These two dictionaries are big, specially the TP and its costly
def Make_TransitionProb_FromTo_Dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	cur2 = con.cursor()
	cur3 = con.cursor()


	from_to_state_dict={}
	TP_dict={}
	# cdef int val


	for val in xrange(75): ## the first 75 states are TB chanin states
		tpbasedict={}
		cur2.execute('select to_state_id , tp_base, is_stratified, stratum_type_id  from transition_probabilities where from_state_id =' + str(val))
		for row2 in cur2:
			if row2[2] == None:
				isstratified=0
				stratifyid=0
			else:
				isstratified=int(row2[2])
				stratifyid=int(row2[3])
				stratdict={}
				cur3.execute('SELECT DISTINCT stratum_name, base from transition_probabilities_by_stratum where from_state_id =' +str(val) + ' and to_state_id= ' + str(row2[0]) )
				for row3 in cur3:
					stratdict[str(row3[0])]=float(row3[1])
					TP_dict[val,row2[0]] = stratdict


			tpbasedict[int(row2[0])]=(row2[1], isstratified, stratifyid)

		from_to_state_dict[val]=tpbasedict
	con.close()
	#print TP_dict
	return (TP_dict,from_to_state_dict)


def Make_TransitionProb_matrix():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	TPMatrix=np.zeros((47,3),dtype='object')
	counter=0
	for i in xrange(24,71):
		T=[]
		S=[]
		cur1.execute('select to_state_id,tp_base from transition_probabilities where from_state_id= ' + str(i))
		for row in cur1:
			S.append(row[0])
			T.append(row[1])


		TPMatrix[counter][0]=i
		TPMatrix[counter][1]=S
		TPMatrix[counter][2]=T
		counter=counter+1


	return TPMatrix
##@package Make_Variables_dict
#@return dictionary of variable made from "varoables" table. keys: variable name, values: value
#@brief  this data is used for tp adjustment
def Make_Variables_dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	coeff_hash={}
	cur1.execute('select   name, value  from variables' )
	for row1 in cur1:
		coeff_hash[str(row1[0].strip())]=float(row1[1])
	con.close()
	return coeff_hash

##@package Make_All_States_dict
#@return dictionary of states made from "states" table. keys: state name, values: state_id
def Make_All_States_dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	States_dict={}
	cur1.execute('select name, id  from states' )
	for row1 in cur1:
		States_dict[str(row1[0].strip())]=int(row1[1])

	con.close()
	return States_dict

##@package Make_States_idname_dict
#@return dictionary of states made from "states" table. keys: state id, values: state name
def Make_States_idname_dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	States_idname_dict={}
	cur1.execute('select   id, name  from states' )
	for row1 in cur1:
		States_idname_dict[row1[0]]=str(row1[1].strip())

	con.close()
	return States_idname_dict

##@package Make_Interaction_states_dict
#@return dictionary of interaction states id and name form "interactions" table containing 27 rows.
#@brief keys: interaction ids, values: interaction name
def Make_Interaction_states_dict():
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	Interaction_states_dict={}
	cur1.execute('select  distinct from_state_id , name from interactions inner join states where  interactions.from_state_id = states.id' )
	for row1 in cur1:
		Interaction_states_dict[int(row1[0])]=str(row1[1].strip())

	con.close()
	return Interaction_states_dict


##@package Make_Intervention_TP_dict
#@return 2D array where the columns are the three tests options and rows are 4 risk factors. the lements are the tuple of sensitivity and specificity values
#@brief Intervention process is defined as going from slow latent, fast latent, Uninfected TB (state isd: 1,2,3) to any of Test option: Infected Testing TST,Infected Testing QFT,Infected Testing TSPOT
# the sensitivity and specificity values that are used to adjust tp for test and treatment are different based on risk factors. This 2D array contain those data for faster access
def Make_Intervention_TP_dict( Variables):
	columns=["Infected Testing TST", "Infected Testing QFT", "Infected Testing TSPOT"]
	rows=['USB','FB','HIV','ESRD']

	Treatment_matrix=np.zeros(shape=(6,4), dtype='float64')
	#TP_coeff=[[0 for x in range(3)] for x in range(4)]  ### rows x columns and each element is [sensitivity, specifity]
	ii=-1
	jj=-1
	for i in rows:
		ii=int(ii+1)
		jj=-1
		for j in columns:
			jj=int(jj+1)
			ss=j.split(' ')[2]
			strval1= str(i) + ' ' + str(ss) + ' ' + 'Sensitivity'
			strval2=str(i) + ' ' + str(ss) + ' ' +'Specificity'
			#TP_coeff[ii][jj]=(Variables[strval1],Variables[strval2])

			#print jj,ii,strval1,strval2,Variables[strval1],Variables[strval2]
			Treatment_matrix[jj][ii]=Variables[strval1]
			Treatment_matrix[jj+3][ii]=(1-Variables[strval2])  ### 1- specificity is used later


	#print "Treatment_matrix ", Treatment_matrix
	#return TP_coeff,Treatment_matrix
	return Treatment_matrix


##@package Make_Interaction_Adjustment_dict
#@return A dictionary of dictionary. keys: combination of from, to states ids, values: dictionary with keys as  in_state_id (which are risk factors) and values: adjustment value.
#@brief There is adjustment value for each transition from state, to state and being in in_state. Those data is been stored in dictionary for faster access.
def Make_Interaction_Adjustment_dict( InteractionDict, Riskfactor_name, Riskfactor_id ):
	# global InteractionDict
	# global Riskfactor_name
	# global Riskfactor_id
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	cur2 = con.cursor()

	IntAdjDict={}
	tempdict={}
	for fromid in InteractionDict:
		#print "from state ids",fromid
		cur1.execute('select distinct  to_state_id  from interactions where from_state_id= ' + str(fromid)  )
		for toid in cur1:
			#print "to state ids",toid
			cur2.execute('select distinct in_state_id, adjustment from interactions where from_state_id= ' + str(fromid) + ' and  to_state_id= ' + str(toid[0]))
			for inid in cur2:
				tempdict[inid[0]]=float(inid[1])
			#print "instate ids", tempdict
			IntAdjDict[fromid,toid[0]]	= tempdict
			tempdict={}
	con.close()
	return IntAdjDict




##@package Intervention_readfile_setupclass
#@return A class of Intervation that is set based on the input intervention's information
#@brief Different intervention methods can be applied in the program. The information for each one is an input data given as a file name. The file is read and information is set into Intervention class
def Intervention_readfile_setupclass():
	f = open("Intervention2.txt",'rU')
	temp=[]
	c=0
	counter=1;
	Cdict={}
	for fi in f:
		c=int(c+1)
		fi.strip()
		t=fi.split(':')
		if t[0] == 'Intervention':
			if c>1:
				Cdict[counter]=temp
				counter=int(counter+1)
				temp=[]
		else:
			temp.append(t[1])

	Cdict[counter]=temp
	f.close()


	I = [Intervention(Cdict[i+1][0],Cdict[i+1][1],Cdict[i+1][2],Cdict[i+1][3],Cdict[i+1][4],Cdict[i+1][5],Cdict[i+1][6],Cdict[i+1][7],Cdict[i+1][8]	) for i in range(counter)]
	return I



##@package Make_Stratum_Name
#@param pi: person object
#@param strataid: stratum_type_id
#@return A stratum name for given person and its stratum_type_id
#@brief each stratum_type_id is associated with unique combination of person attributes and risk factors
def Make_Stratum_Name(pi, strataid):
	StratumType_dict={}
	StratumType_dict[0]=['sex','age_group']
	StratumType_dict[1]=['years_in_us', 'birthplace','sex', 'race', 'age_group']
	StratumType_dict[2]=['sex', 'race', 'age_group', 'years_in_us']
	StratumType_dict[3]=['sex','race', 'age_group']
	StratumType_dict[4]=['Homeless','sex', 'race', 'age_group']
	StratumType_dict[5]=['Diabetes' ,'sex', 'race', 'age_group']
	StratumType_dict[6]=[ 'sex', 'HIV_ART' ,'race', 'age_group']
	StratumType_dict[7]=['sex']
	StratumType_dict[8]= ['years_in_us', 'ESRD','HIV_ART']

	Strstrata=''
	strata_id_dict={'sex':1,'age_group':3,'years_in_us':5,'birthplace':6,'race':2,}
	if strataid == 0 or strataid == 1 or  strataid == 2 or strataid == 3 or strataid == 7:
		for si in StratumType_dict[strataid]:
			#Strstrata=Strstrata + str(getattr(pi, si)) + ' '
			indxtemp=strata_id_dict[si]
			Strstrata=Strstrata + str(pi[indxtemp]) + ' '

	elif strataid == 4:
		if pi[15] == 1:
			Strstrata='Homeless' +' ' + str(pi[1]) + ' ' + str(pi[2]) + ' ' + str(pi[3])
		else:
			Strstrata='Not homeless' + ' ' + str(pi[1]) + ' ' + str(pi[2]) + ' ' + str(pi[3])

	elif strataid == 5:
		if pi[23] == 1:
			Strstrata='Diabetes' + ' ' + str(pi[1]) + ' ' + str(pi[2]) + ' ' + str(pi[3])
		else:
			Strstrata='No diabetes'  + ' ' + str(pi[1]) + ' ' + str(pi[2]) + ' ' + str(pi[3])

	elif strataid == 6:
		if pi[19] == 1:
			Strstrata=  str(pi[1]) + ' ' + 'Infected HIV, ART' + ' ' + str(pi[2]) + ' ' + str(pi[3])
		else:
			Strstrata=str(pi[1]) + ' ' + 'Uninfected HIV' + ' ' + str(pi[2]) + ' ' + str(pi[3])

	elif strataid == 8:
		if pi[16] == 1 and pi[19]==1:
			Strstrata=  str(pi[5]) + ' ' + 'ESRD' + ' ' + 'Infected HIV, ART'
		elif pi[16] == 1 and pi[19]==0:
			Strstrata=  str(pi[5]) + ' ' + 'ESRD' + ' ' + 'Uninfected HIV'
		elif pi[16] == 0 and pi[19]==0:
			Strstrata=  str(pi[5]) + ' ' + 'No ESRD' + ' ' + 'Uninfected HIV'
		elif pi[16] == 0 and pi[19]==1:
			Strstrata=  str(pi[5]) + ' ' + 'No ESRD' + ' ' + 'Infected HIV, ART'


	Strstrata=Strstrata.strip() ## to remove the extra space at the end
	return Strstrata



##@package Population_Sample
#@param PopulationNumber: Number of individuals in population
#@param New  is been set if its been called for newcomers for open cohort.
#@param year  for initial step, its the year we choose to strat the program. For newcomers its the year of having newcomers.
#@return return the index and weight for each index of the base_init_lines table
#@brief this index values are used to assign the race, sex, ... for initial people
def Population_Sample(PopulationNumber,New,year):
	con = lite.connect('./limcat-zero-index.sqlite')
	cur1 = con.cursor()
	cur2=con.cursor()


	if New :  ### it means newcommers and New is True

		column='weight_new_people' + str(year)
		cur1.execute('select `index`, ' + column + ' from base_init_lines')
		cur2.execute('select sum(' + column + ') from base_init_lines')
		total=cur2.fetchone()   ## sum of all weights
		total=total[0]
	else:
		cur1.execute('select `index`, weight'+str(year)+ '  from base_init_lines')
		cur2.execute('select sum(weight'+str(year)+')  from base_init_lines')
		total=cur2.fetchone()   ## sum of all weights
		total=total[0]




	elements = []
	weights = []

	for row in cur1:
		elements.append(row[0])
		if row[1] != None:  ### There is no weight for some records
			weights.append(row[1] / float(total)) ## get the percentage of weight for each index
		else:
			weights.append(0)

	A=np.random.choice(elements, PopulationNumber, p=weights)
	### A contains the index of the base_init_line table that we have to choose people from based on the weight and population size
	con.close()
	return   A

##@package  Initial_Person_from_dict
#@param Pop_Sample is the list created from "Population_Sample" function, containing the index of the people from "base_init_lines" table
#@return person's object with set attributes (non randomize one)
#@brief Person calss's attributes (non randomiz chain values as: sex, age, ...) are set .The age is set as months not years to easy access from dictionary. The index values are used to assign the race, sex, ... for initial people. Age above 35 is considered as riskfactor, so its set here.
# the Susceptible_ActiveCase_dict is also been set here. This dictionary vallues is been used later for "Active case finding"
def Initial_Person_from_dict(P,ci, Pop_Sample,  Initial_People_Dict,Riskfactor_id,Riskfactor_name, Susceptible_ActiveCase_dict):
	# global Initial_People_Dict
	# global Riskfactor_id
	# global Riskfactor_name
	# global Susceptible_ActiveCase_dict



	counter=-1
	for i in xrange(len(P)):

		counter=counter+1

		row=Initial_People_Dict[Pop_Sample[counter]]

		# print "=======", P[i], "======="
		# print "*******", i,P[i][0]
		P[i][0]=counter
		#print "Initial person ", len(P), counter, P[i][0]
		P[i][1]=str(row[0].strip())
		P[i][2]=str(row[1].strip())
		P[i][3]=str(row[2].strip())
		P[i][4]=str(row[3].strip())
		P[i][5]=str(row[4].strip())
		P[i][6]=str(row[5].strip())



		if row[5] == 'United States' or row[3] == 'Born in US':
			P[i][7]=1


		#### Age is set low value in age range
		B=row[2].split(' ')
		a=int(B[1][0:2])

		P[i][10]=a *12  ### convering the year to month as age
		#print "***** age", a,a*12, P[i][10]
		#if a >= 35: ## age above 35 is also risk factor
			#P[i][26]=1

		##pi.age_group =  Age_Group_Dict[pi.age]  @@@ fekr konam in lazem nist chon aval agegroup bar asase table set shode


		## set the state id to 0, uninitialized states
		P[i][8]=0   ###Uninitialized
		P[i][9]='Uninitialized'
		#print "ci ", ci
		temparr=[0]*(ci-1)
		P[i][14]=temparr #######@@@@@@

		####@@@@@ have to change later sinceits been set for first intervention now
		P[i][13]=1

		###setup susceptible and activecase dictionary
		###The keys are the combination of brithplace and race and values are initialized as 0. later in program based on number susceptible and active cases these value increase.
		#####Susceptibleval=(str(P[i][6].strip()),str(P[i][2].strip()))

		# Susceptibleval=(str(P[i][7]),str(P[i][2].strip()))
		# #print "Susceptibleval ", Susceptibleval
		# if Susceptibleval not in Susceptible_ActiveCase_dict.keys():
		# 	Susceptible_ActiveCase_dict[Susceptibleval]=[0,0.0]

	return P

##@package  Set_InitialPerson_Riskfactors
#@param people in the program as class objects
#@return people in the program as class objects where the risk factor is been set up
#@brief risk factors or randomize chains are set in this function. Each person can randomly assign to have any of the risk factors
#age_group is also one of the risk factors, but that is been automativcally set when a person is in risk factor age group.
def Set_InitialPerson_Riskfactors(P,Riskfactor_id,Riskfactor_name, RiskFactor_StratumType_dict,  RiskFactor_TPvale_dict):
	# global Riskfactor_id
	# global Riskfactor_name
	# global RiskFactor_StratumType_dict
	# global RiskFactor_TPvale_dict
    ### Keys :"Smoker","Homeless""ESRD""TNF-alpha""Alcohol""Diabetes""Infected HIV, no ART""Infected HIV, ART""IDU" "Transplant patient"
	### array index [24,15,16,17,18,23,19,20,22,21]
	Key_index_dict={194:21, 179:23, 74:24,183:19,78:15, 83:16,87:17,184:20,91:18,189:22}
	#riskfactorindex=[24,15,16,17,18,23,19,20,22,21]
	for pi in xrange(len(P)):
		#print "Person ", pi
		counter=-1
		for i in RiskFactor_StratumType_dict.keys():  ### loop over  riskfactors : stratum_type_id
			#print "+++ ", i, RiskFactor_StratumType_dict.keys()
			counter=counter+1
			#print "Risk factor ", counter
			stratname=Make_Stratum_Name(P[pi],RiskFactor_StratumType_dict[i]) #### stratum_type_id
			keyval=(i,stratname)
			if keyval in RiskFactor_TPvale_dict.keys():
				riskval=float(RiskFactor_TPvale_dict[i,stratname])
				r=float(random.uniform(0.0,1.0))

				if r < riskval: ### randomly set the risk factor for person
					#print "******* RF", pi, i, keyval[0], Key_index_dict, Key_index_dict[keyval[0]]
				#	print "Initial RF ", P[pi][riskfactorindex[counter]], riskfactorindex[counter]
					#setattr(pi, Riskfactor_name[counter],1)
					#P[pi][riskfactorindex[counter]]=1
					P[pi][Key_index_dict[keyval[0]]]=1
					P[pi][26]=1
					#print "Person RF ", P[pi][riskfactorindex[counter]]

	return P







def Initializing_people( PopulationNumber,ci, Riskfactor_id,Riskfactor_name,  RiskFactor_TPvale_dict,  Susceptible_ActiveCase_dict,  RiskFactor_StratumType_dict,  Initial_People_Dict,Flagy):
	#cdef int i
	#P = [person() for i in range(PopulationNumber)]
	####3@@@@@ Couldn't get hoe define dtype of unknown size subarray for statelist, for known size :(2,)int8
	#P = np.zeros(shape=(PopulationNumber,29),  dtype='int8,str,str,str,str,str,str,int8,int8,str,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8,int8 ')

	#P = np.zeros(shape=(PopulationNumber,),  dtype=[('f0', 'int32'), ('f1', 'S50'), ('f2', 'S50'), ('f3', 'S50'), ('f4', 'S50'), ('f5', 'S50'), ('f6', 'S50'), ('f7', 'i1'), ('f8', 'int32'), ('f9', 'S50'), ('f10', 'int32'), ('f11', 'i1'), ('f12', 'int32'), ('f13', 'i1'), ('f14', '(120,)int32'), ('f15', 'i1'), ('f16', 'i1'), ('f17', 'i1'), ('f18', 'i1'), ('f19', 'i1'), ('f20', 'i1'), ('f21', 'i1'), ('f22', 'i1'), ('f23', 'i1'), ('f24', 'i1'), ('f25', 'i1'), ('f26', 'i1'), ('f27', 'i1'), ('f28', 'i1')])
	P = np.zeros(shape=(PopulationNumber,29),  dtype=object)

	# P[:,[27]]=1  ###3 it should work but gives error, need to be check later
	# print "------------",P
	for i in xrange(len(P)):
		P[i][27]=1
	#print "*********", P
	dd=ci/12
	if dd <14 :
		yearval=2001+dd
	else:
		yearval=2014
	Pop_Sample=Population_Sample(PopulationNumber,Flagy,yearval)

	
	#Pop_Sample=Population_Sample(PopulationNumber,False,2001)


	P=Initial_Person_from_dict(P,ci, Pop_Sample,Initial_People_Dict,Riskfactor_id,Riskfactor_name, Susceptible_ActiveCase_dict)
	#Initial_People_Dict.clear()

	#P=Set_InitialPerson_Riskfactors(P,Riskfactor_id,Riskfactor_name, RiskFactor_StratumType_dict, RiskFactor_TPvale_dict)

	### just delete for graph generating
	# pool = Pool()
	# alen = len(P)
	# start=0
	# first=alen/4
	# second=2*alen/4
	# third=3*alen/4
	# fourth= alen ###2 * alen/3

	P=Set_InitialPerson_Riskfactors(P,Riskfactor_id,Riskfactor_name, RiskFactor_StratumType_dict, RiskFactor_TPvale_dict)

	# r1 = pool.apply_async(Set_InitialPerson_Riskfactors,[P[start:first],Riskfactor_id,Riskfactor_name, RiskFactor_StratumType_dict, RiskFactor_TPvale_dict])
	# r2 = pool.apply_async(Set_InitialPerson_Riskfactors,[P[first:second],Riskfactor_id,Riskfactor_name, RiskFactor_StratumType_dict, RiskFactor_TPvale_dict])
	# r3 = pool.apply_async(Set_InitialPerson_Riskfactors,[P[second:third],Riskfactor_id,Riskfactor_name, RiskFactor_StratumType_dict, RiskFactor_TPvale_dict])
	# r4 = pool.apply_async(Set_InitialPerson_Riskfactors,[P[third:fourth],Riskfactor_id,Riskfactor_name, RiskFactor_StratumType_dict, RiskFactor_TPvale_dict])
	# answer1 = r1.get()
	# answer2 = r2.get()
	# answer3 = r3.get()
	# answer4 = r4.get()
	# P=answer1+answer2 +answer3+answer4

	#RiskFactor_StratumType_dict.clear()
	#RiskFactor_TPvale_dict.clear()

	return P
