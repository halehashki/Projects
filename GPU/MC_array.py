#!/usr/bin/env python


import sqlite3 as lite
import random
import numpy as np
import time
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
import pycuda.driver as cuda
import pycuda.autoinit
from numpy import *
from pycuda.elementwise import ElementwiseKernel
from numpy.linalg import *
import time
from pycuda import driver, compiler, gpuarray, tools
import pycuda.curandom as curandom
from collections import Counter
import threading
####http://stackoverflow.com/questions/27563236/what-is-the-total-thread-countexecuted-over-time-not-parallel-for-cuda
from functools import reduce

class GPUThread_matrixmul(threading.Thread) :
    def __init__(self, number, a_cpu,d_cpu):
        threading.Thread.__init__(self)

        self.number = number
        self.a_cpu = a_cpu
	self.d_cpu = d_cpu

	self.out = np.zeros(len(d_cpu) , dtype='float64')


    def run(self):
        self.dev = cuda.Device(self.number)
        self.ctx = self.dev.make_context()

	self.out=multiply_matrix_vector(self.a_cpu,self.d_cpu)

        print "successful exit from thread %d" % self.number
	self.ctx.pop()

    def __del__(self):
        del self.a_cpu
	del self.d_cpu
        del self.ctx
	del self.out



class GPUThread_Nextstep(threading.Thread) :
    def __init__(self, number, TP_matrix,S_matrix):
        threading.Thread.__init__(self)

        self.number = number
        self.TP_matrix=TP_matrix
	self.S_matrix=S_matrix


	self.out = np.zeros(len(self.TP_matrix) , dtype='float64')


    def run(self):
        self.dev = cuda.Device(self.number)
        self.ctx = self.dev.make_context()

	self.out=cal_next_step(self.TP_matrix,self.S_matrix)

        print "successful exit from thread %d" % self.number
	self.ctx.pop()

    def __del__(self):
        del self.TP_matrix
	del self.S_matrix

        del self.ctx
	del self.out



class GPUThread_CalRisk(threading.Thread) :
    def __init__(self, number, a_cpu,b_cpu,generalPopulationRisk):
        threading.Thread.__init__(self)

        self.number = number
        self.a_cpu=a_cpu
	self.b_cpu=b_cpu
	self.generalPopulationRisk=generalPopulationRisk


	self.out = np.zeros(len(b_cpu) , dtype='float64')


    def run(self):
        self.dev = cuda.Device(self.number)
        self.ctx = self.dev.make_context()

	self.out=cal_risk_val(self.a_cpu,self.b_cpu,self.generalPopulationRisk)

        print "successful exit from thread %d" % self.number
	self.ctx.pop()

    def __del__(self):
        del self.a_cpu
	del self.b_cpu
        del self.generalPopulationRisk
        del self.ctx
	del self.out




def multiply_matrix_vector(a_cpu,d_cpu):
	mod = SourceModule( """
    __global__ void matvec(double *vec, double *mat, double *out, const int row, const int col){

       double sum=0;  // doulbe is also not working

     for (int tid = threadIdx.x + blockIdx.x*blockDim.x;
                tid < row;
                tid +=gridDim.x * blockDim.x){

                for(int i=0; i < col; i++)
                   sum += mat[(tid*col) + i] * vec[i];
        out[tid]=sum;
        }
    }
    """)
	matvec = mod.get_function("matvec")

    	blocks=8
    	block_size=1024
    	MATRIX_SIZE=len(d_cpu) #matsize
    	VECTOR_SIZE=10 ##len(a) vectro a
	#print "in function lend ", MATRIX_ZISE
    	a_gpu = gpuarray.to_gpu(a_cpu)
    	d_gpu = gpuarray.to_gpu(d_cpu)

   	c_gpu = gpuarray.zeros((MATRIX_SIZE), np.float64)

    	matvec(a_gpu,d_gpu,c_gpu,np.int32(MATRIX_SIZE),np.int32(VECTOR_SIZE), grid=(blocks,1), block=(block_size,1,1) )

    	c_cpu=c_gpu.get()
	#print "in function ", c_cpu
	return c_cpu



def cal_next_step(TP_matrix,S_matrix):
	mod = SourceModule( """
    __global__ void nextstep(double *TP, double  *S, double *out, float *r,const int row,const int col){
        for (int tid = threadIdx.x + blockIdx.x*blockDim.x;
    	    tid < row;
    	    tid +=gridDim.x * blockDim.x){

            for(int i=0; i < col-1; i++){
                   // out[tid]=TP[(tid*col) + i];
                      if (TP[(tid*col) + i] < r[tid]) out[tid]=S[(tid*col) + i+1];

            //           if (TP[(tid*col) + i] < r[tid]) out[tid]=i+1;
    }
    }
    }

    """)
	nextstep = mod.get_function("nextstep")
    	psize=len(TP_matrix)
    	Row=psize
	Col=5
	blocks=8
	block_size=1024

    	r_gpu=curandom.rand(psize,dtype=np.float32 )

	#begintime=time.time()
	TP_gpu = gpuarray.to_gpu(TP_matrix)
	S_gpu = gpuarray.to_gpu(S_matrix)

	c_gpu=gpuarray.zeros(psize, dtype='float64')

	nextstep(TP_gpu,S_gpu,c_gpu,r_gpu,np.int32(Row),np.int32(Col), grid=(blocks,1), block=(block_size,1,1) )
    	c_cpu=c_gpu.get()

	return c_cpu



def cal_risk_val(a_cpu,b_cpu,generalPopulationRisk):
	mod = SourceModule( """
    __global__ void riskcal(double *a, double *b, double *out, const double generalrisk, const int row)
    {
    	for (int tid = threadIdx.x + blockIdx.x*blockDim.x;
                tid < row;
                tid +=gridDim.x * blockDim.x){

        out[tid]=(a[tid]/b[tid]*0.8 + generalrisk) * 4.0;
    }
    }

    """)
	riskcal = mod.get_function("riskcal")
        bsize=len(a_cpu)
    	a_gpu=gpuarray.to_gpu(a_cpu)
 	b_gpu=gpuarray.to_gpu(b_cpu)
	c_gpu=gpuarray.zeros((bsize,),dtype=np.float64)
#
	blocks=8
	block_size=1024
    	Row=bsize

	riskcal(a_gpu,b_gpu,c_gpu,np.float64(generalPopulationRisk),np.int32(Row), grid=(blocks,1), block=(block_size,1,1) )
	c_cpu=c_gpu.get()



	return c_cpu











def Make_Next_Step_Matrix(P,ci, Intervention,STP_matrix,Treatment_matrix,ActivacaseRPval,Susceptible_ActiveCase_dict,test_choice_pos,test_choice_neg,treatment_choice_pos,treatment_choice_neg,MonthlyUptake):

	S_matrix=np.zeros((len(P),5), dtype='float64')
	TP_matrix=np.zeros((len(P),5), dtype='float64')

	b=np.where(np.logical_and(P[:,8]==1,P[:,27]==1)) ### state=1

	#### Transmission calculation
	totalSusceptible = len(b[0])

	totalActive= ActivacaseRPval
	generalPopulationRisk = float(float(totalActive / totalSusceptible) * 0.2)
#	print " generalPopulationRisk ",  generalPopulationRisk

	Tneg=[0,0]
	Tpos=[0,0]
	Uptake=[0.0,0.0]
	risk=0.0



	Uptake=MonthlyUptake
	Tneg=test_choice_neg

	begintime=time.time()

	mykeys=zip(P[b[0],7],P[b[0],2])

	#####COUNT THE NUMBER OF SUSCEPTIBLE FOR EACH GROUP
	c = Counter(mykeys)

	counter=-1
	susceptiblearr=np.zeros(len(b[0]), dtype='float64')
	#susceptiblearr=[0]*len(b[0])
	for i in mykeys:
		counter=counter+1
		susceptiblearr[counter]=c[i]

	activearr=np.asarray([Susceptible_ActiveCase_dict[x] for x in mykeys])



 	a_cpu=np.ascontiguousarray(activearr)
 	b_cpu=np.ascontiguousarray(susceptiblearr)

    	#bsize=len(b[0])
    	alen=len(b[0])
    	start=0
        first=alen/4
        second=2*alen/4
        third=3*alen/4
    	fourth= alen
    	cuda.init()
        #print "ghabl az gpu",start, first, second,third,fourth, a_cpu[start:first],d_cpu[start:first]
    	gpu_thread1 =  GPUThread_CalRisk(0, a_cpu[start:first],b_cpu[start:first],generalPopulationRisk)
        gpu_thread1.run()

    	gpu_thread2 =  GPUThread_CalRisk(1, a_cpu[start:first],b_cpu[first:second],generalPopulationRisk)
    	gpu_thread2.run()

    	gpu_thread3 =  GPUThread_CalRisk(2, a_cpu[start:first],b_cpu[second:third],generalPopulationRisk)
    	gpu_thread3.run()

        gpu_thread4 =  GPUThread_CalRisk(3, a_cpu[start:first],b_cpu[third:fourth],generalPopulationRisk)
    	gpu_thread4.run()

	#print "++++  threading1", gpu_thread1.out
	#print "++++  threading2", gpu_thread2.out
	#print "++++  threading3", gpu_thread3.out
	#print "++++  threading4", gpu_thread4.out
	Risklist=np.concatenate([gpu_thread1.out, gpu_thread2.out, gpu_thread3.out,gpu_thread4.out])
	#RisklistThread=gpu_thread1.out + gpu_thread2.out+ gpu_thread3.out+gpu_thread4.out
	#print "++++  threading risk list " , RisklistThread

   	#Risklist=cal_risk_val(a_cpu,b_cpu,generalPopulationRisk)
    	#print "GPU ", Risklist



	RiskAverage=(sum(Risklist) / float(len(Risklist)))




	S_matrix[b[0],0]=Tneg[0] ## first element is uptake value for test
	S_matrix[b[0],1]=Tneg[1]
	S_matrix[b[0],2]=1
	S_matrix[b[0],3]=2

	TP_matrix[b[0],0]=Uptake[0] ## first element is uptake value for test
	TP_matrix[b[0],1]=Uptake[1]
	TP_matrix[b[0],2]=.99
	TP_matrix[b[0],3]=Risklist



		#####@@@@ for people in state 2, only goes to 2 and 63, test
	b=np.where(np.logical_and(P[:,8]==2, P[:,27] ==1)) ### state=2

	Tpos=[0,0]
	Uptake=[0.0,0.0]

	##interaction calculation
	a=[1.0,11.0,4.7,1.0,5.4,5.4,2.4,0.0,1.1,2.5]   ### adjustment for risk factore in order from 15  to 24  { IDU has 0.0 adjustment value}


	#if ci > 2:
	Tpos=test_choice_pos
	Uptake=MonthlyUptake


	TPadjustlist=[6.08536966506534e-05]*len(b[0])
	counter=-1

	if len(b[0]) > 0:
	     #a_cpu=np.asarray(a)
	     #d=P[b[0],15:25]
	     a_cpu=np.array(a, dtype=float64)
             d=P[b[0],15:25]

             #d_cpu=np.asarray(d)
             d_cpu=np.array(d, dtype=float64)
	     #print "===== len d", len(b[0]), len(d)
	     #d_cpu=np.asarray(d)
		 ###### GPU threading
	     if len(b[0]) > 1000:
	     	alen=len(d)
	     	start=0
             	first=alen/4
             	second=2*alen/4
             	third=3*alen/4
 	     	fourth= alen
	     	cuda.init()
                #print "ghabl az gpu",start, first, second,third,fourth, a_cpu[start:first],d_cpu[start:first]
	     	gpu_thread1 =  GPUThread_matrixmul(0, a_cpu,d_cpu[start:first])
             	gpu_thread1.run()

	     	gpu_thread2 =  GPUThread_matrixmul(1, a_cpu,d_cpu[first:second])
	     	gpu_thread2.run()

	     	gpu_thread3 =  GPUThread_matrixmul(2, a_cpu,d_cpu[second:third])
	     	gpu_thread3.run()

             	gpu_thread4 =  GPUThread_matrixmul(3, a_cpu,d_cpu[third:fourth])
	     	gpu_thread4.run()

		#print "++++  threading1", gpu_thread1.out
		#print "++++  threading2", gpu_thread2.out
		#print "++++  threading3", gpu_thread3.out
		#print "++++  threading4", gpu_thread4.out
		c_cpu=np.concatenate([gpu_thread1.out, gpu_thread2.out, gpu_thread3.out,gpu_thread4.out]) 
	    	#c_cpuThread=gpu_thread1.out + gpu_thread2.out + gpu_thread3.out + gpu_thread4.out
        	#print "++++  threading matrixvector  " , c_cpuThread

		#del (gpu_thread1.out)
	        #del (gpu_thread2.out)
             	#del (gpu_thread3.out)
             	#del (gpu_thread4.out)
	     	#print "++++++ treading ", c_cpu
	     else:

	        c_cpu=multiply_matrix_vector(a_cpu,d_cpu)
	        #print "------- GPU ", c_cpu

	     c_cpu[c_cpu == 0] = 1.0
	     TPadjustlist=np.multiply(TPadjustlist,c_cpu)




	S_matrix[b[0],0]=Tpos[0] ## first element is uptake value for test
	S_matrix[b[0],1]=Tpos[1]
	S_matrix[b[0],2]=2
	S_matrix[b[0],3]=63

	TP_matrix[b[0],0]=Uptake[0] ## first element is uptake value for test
	TP_matrix[b[0],1]=Uptake[1]
	TP_matrix[b[0],2]=0.9999391463
	TP_matrix[b[0],3]=TPadjustlist


	####@@@@ state 3 goes to 1,3,63,test
	a=[1.0,11.0,4.7,1.0,5.4,5.4,2.4,0.0,1.6,2.5]
	b=np.where(np.logical_and(P[:,8]==3, P[:,27] ==1)) ### state=3
	Tpos=[0,0]
	Uptake=[0.0,0.0]


	#if ci>2:
	Tpos=test_choice_pos
	Uptake=MonthlyUptake


	TPadjustlist=[6.08536966506534e-05]*len(b[0])
	counter=-1

	if len(b[0]) > 0:
		# a_cpu=np.asarray(a)
		# d=P[b[0],15:25]
        #
		# d_cpu=np.asarray(d)
             a_cpu=np.array(a, dtype=float64)
             d=P[b[0],15:25]

             #d_cpu=np.asarray(d)
             d_cpu=np.array(d, dtype=float64)
	     #print "===== len d", len(b[0]), len(d)
	     #d_cpu=np.asarray(d)
		 ###### GPU threading
	     if len(b[0]) > 1000:
	     	alen=len(d)
	     	start=0
             	first=alen/4
             	second=2*alen/4
             	third=3*alen/4
 	     	fourth= alen
	     	cuda.init()
                #print "ghabl az gpu",start, first, second,third,fourth, a_cpu[start:first],d_cpu[start:first]
	     	gpu_thread1 =  GPUThread_matrixmul(0, a_cpu,d_cpu[start:first])
             	gpu_thread1.run()

	     	gpu_thread2 =  GPUThread_matrixmul(1, a_cpu,d_cpu[first:second])
	     	gpu_thread2.run()

	     	gpu_thread3 =  GPUThread_matrixmul(2, a_cpu,d_cpu[second:third])
	     	gpu_thread3.run()

             	gpu_thread4 =  GPUThread_matrixmul(3, a_cpu,d_cpu[third:fourth])
	     	gpu_thread4.run()

		#print "++++  threading1", gpu_thread1.out
		#print "++++  threading2", gpu_thread2.out
		#print "++++  threading3", gpu_thread3.out
		#print "++++  threading4", gpu_thread4.out
		c_cpu=np.concatenate([gpu_thread1.out, gpu_thread2.out, gpu_thread3.out,gpu_thread4.out]) 
		#c_cpuThread=gpu_thread1.out+gpu_thread2.out+gpu_thread3.out+gpu_thread4.out
		#print "+++++ threading matrix vect ", c_cpuThread
        	#####c_cpu=multiply_matrix_vector(a_cpu,d_cpu)
        	#print "GPU  ", c_cpu
		c_cpu[c_cpu == 0] = 1.0
		TPadjustlist=np.multiply(TPadjustlist,c_cpu)

	    else:
		c_cpu=multiply_matrix_vector(a_cpu,d_cpu)

	    

	S_matrix[b[0],0]=Tpos[0] ## first element is uptake value for test
	S_matrix[b[0],1]=Tpos[1]
	S_matrix[b[0],2]=1
	S_matrix[b[0],3]=3
	S_matrix[b[0],4]=63

	TP_matrix[b[0],0]=Uptake[0] ## first element is uptake value for test
	TP_matrix[b[0],1]=Uptake[1]
	TP_matrix[b[0],2]=0.00168214255273957
	TP_matrix[b[0],3]=0.99825700375
	TP_matrix[b[0],4]=TPadjustlist



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
			if len(temparr[0]) > 0:
				SS=STP_matrix[temparr[0][0]][1]  #### S to S
				TT=STP_matrix[temparr[0][0]][2]  ### T to T

				S_matrix[i][0:len(SS)]=SS  #### S to S
				TP_matrix[i][0:len(TT)]=TT  ### T to T


		##### caling activation at the end
	S_matrix, TP_matrix=Activation(P,S_matrix, TP_matrix)
	###Normalizing
	row_sums = TP_matrix.sum(axis=1)
	#print "--- TO_matrix" , TP_matrix
	TP_matrix = TP_matrix / row_sums[:, np.newaxis]


	for i in xrange(len(TP_matrix)):  ### maybe parallel
		sortinds=TP_matrix[i].argsort()  ## sorting T list and then sort S based on the sorted indices
		TP_matrix[i]=TP_matrix[i][sortinds]
		S_matrix[i]=S_matrix[i][sortinds]



	return S_matrix, TP_matrix, RiskAverage





def Activation(P,S_matrix, TP_matrix):
	pp=np.where(P[:,27]==1)
	pi1=np.where(np.logical_and(P[:,12] < 36, P[:,12] != 0))
	pi2=np.where(np.logical_or(P[:,8] <= 61, P[:,8] >=72))
	pi3=np.intersect1d(pi1[0],pi2[0])
	pi=np.intersect1d(pi3,pp)


	if len(pi) >0:
		for i in pi:

			Tarr=S_matrix[i] ### the state probability array
			sindx=np.where(Tarr == 63) ###63: active untreated
			if len(sindx[0]) > 0: ### it exist

				TP_matrix[i][sindx[0]]=TP_matrix[i][sindx[0]]*13.305108

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
			matrixrow= int(P[i][8] - 4)

		else :
			matrixrow= int(P[i][8] - 6)  ### state -6 ar ethe matrix indices : 9 -> 3, ...
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


def Assign_Next_Step(P, S_matrix, TP_matrix, Dead):

	TP_matrix=np.cumsum(TP_matrix, axis=1)

    	alen=len(P)
    	start=0
        first=alen/4
        second=2*alen/4
        third=3*alen/4
    	fourth= alen
    	cuda.init()
        #print "ghabl az gpu",start, first, second,third,fourth, a_cpu[start:first],d_cpu[start:first]
    	gpu_thread1 =  GPUThread_Nextstep(0, TP_matrix[start:first],S_matrix[start:first])
        gpu_thread1.run()

    	gpu_thread2 =  GPUThread_Nextstep(1, TP_matrix[start:first],S_matrix[first:second])
    	gpu_thread2.run()

    	gpu_thread3 =  GPUThread_Nextstep(2, TP_matrix[start:first],S_matrix[second:third])
    	gpu_thread3.run()

        gpu_thread4 =  GPUThread_Nextstep(3, TP_matrix[start:first],S_matrix[third:fourth])
    	gpu_thread4.run()

	#print "++++  threading1", gpu_thread1.out
	#print "++++  threading2", gpu_thread2.out
	#print "++++  threading3", gpu_thread3.out
	#print "++++  threading4", gpu_thread4.out
	newStates=np.concatenate([gpu_thread1.out, gpu_thread2.out, gpu_thread3.out,gpu_thread4.out]) 
	#newThread=gpu_thread1.out+gpu_thread2.out+gpu_thread3.out+gpu_thread4.out
        #print "+++++ threading new state ", newThread

    	#print "---- TO CHECK ", len(P), len(TP_matrix)
	#####NewStates=cal_next_step(TP_matrix,S_matrix)
    	#print "GPU  NEW STATES ", NewStates
	#print "---------------------------------------------- Next state", NewStates
	P[:,8]=NewStates



	b=np.where(np.logical_and(P[:,8]==2,P[:,27]==1))
	for i in xrange(len(b[0])):
		if P[i][12] == 0:  #### meaning its new to states 2, otherwise its been in this states
			P[i][12]=round(random.uniform(0.0,1.0) * 36)


	b=np.where(np.logical_and(P[:,8]==3,P[:,27]==1))
	P[b[0],12]=1000
	#print "======= assign states 3", len(b[0]) , P[b[0],12]
	b=np.where(np.logical_and(P[:,8]==30,P[:,27]==1))
	P[b[0],12]=1000


	for i in xrange(len(P)):
		P[i][14].append(NewStates[i])

	b=np.where(np.logical_and(P[:,8]==72,P[:,27]==1))
	P[b[0],27]=0 ###Is died

	Dead=Dead + len(b[0])

	return P, Dead



def Cal_RiskOfProgression(P, S_matrix, TP_matrix,Susceptible_ActiveCase_dict):
	####@@@@@ Ignored efficacy calculation for now, maybe add it later, since Alex doesn't have that it might not change a lot
	RiskOfProgression=0.0

	pp=np.where(P[:,27]==1) ## only alive people
	RPi1=np.where(np.logical_and((P[:,8] >=2) ,(P[:,8] <=8)))
	RPi2=np.where(np.logical_and((P[:,8] >=14) , (P[:,8] <=39)))
	RPi3=np.where(P[:,8]==62)


	RPi4=np.concatenate((RPi1[0],RPi2[0],RPi3[0]),axis=0)

	RPi=np.intersect1d(RPi4,pp[0])
	#print "RP ", len(RPi)

	P[RPi,12]=P[RPi,12]+1
	######@@@@ maybe better or faster to get all ST_matrix of given index in temporary array and do the rest of thing
	for mi in RPi:

		S= S_matrix[mi]
		T= TP_matrix[mi]

		if 63 in S:
			indx=np.where(S==63)
			sindx=indx[0][0]
			Rval=T[sindx]
			j=mi

			### new set up using US born/FB born instead of bp
			#Susceptible_ActiveCase_dict[str(P[j][7]),P[j][2]][1]=float(Susceptible_ActiveCase_dict[str(P[j][7]),P[j][2]][1]+Rval)
			#Susceptible_ActiveCase_dict[P[j][7],P[j][2]][1]=float(Susceptible_ActiveCase_dict[P[j][7],P[j][2]][1]+Rval)
			Susceptible_ActiveCase_dict[P[j][7],P[j][2]]=float(Susceptible_ActiveCase_dict[P[j][7],P[j][2]]+Rval)

			RiskOfProgression=RiskOfProgression+Rval



	return RiskOfProgression,Susceptible_ActiveCase_dict

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
	b=np.where(np.logical_and(P[:,19]==0,P[:,27]==1))  ### no diabeties
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
	indx=np.where( randarr <  0.004309472 )
	P[indx[0],24]=0
	P[indx[0],26]=1

	#### No ESRD to ESRD ( adjustment for having Diabetes)
	pi1=np.where(P[:,27]==1)
	pi2=np.where(np.logical_and(P[:,16]==0,P[:,24]==1)) ## and having diabeties
	b=np.intersect1d(pi1[0],pi2[0])


	if len(b) >0 :
		randarr= np.random.uniform(0.0,1.0,len(b))
		indx=np.where( randarr <  10.4 * 8.9802e-06 )
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
		#print P[i][3]
		if P[i][3] == 'Age 35-39':
			tpadj= 8.9802e-06 * adjval[0]
		elif  P[i][3] == 'Age 40-44':
			tpadj= 8.9802e-06 * adjval[1]
		elif  P[i][3] == 'Age 45-49':
			tpadj= 8.9802e-06 * adjval[2]
		elif  P[i][3] == 'Age 50-54':
			tpadj= 8.9802e-06 * adjval[3]
		elif  P[i][3] == 'Age 55-59':
			tpadj= 8.9802e-06 * adjval[4]
		elif  P[i][3] == 'Age 60-64':
			tpadj= 8.9802e-06 * adjval[5]
		elif  P[i][3] == 'Age 65-69':
			tpadj= 8.9802e-06 * adjval[6]
		elif  P[i][3] == 'Age 70-74':
			tpadj= 8.9802e-06 * adjval[7]
		elif  P[i][3] == 'Age 75-79':
			tpadj= 8.9802e-06 * adjval[8]
		elif  P[i][3] == 'Age 80+':
			tpadj= 8.9802e-06 * adjval[9]
		else:
			tpadj= 8.9802e-06

		#print "++++", i, tpadj
		randarr= np.random.uniform(0.0,1.0)
		if  randarr <  tpadj :
			P[indx[0],17]=1
			P[indx[0],26]=1


	for i in xrange(len(P)):
		if P[i][27] ==1 :
			P[i][10]=int(P[i][10] + cycle_duration)

			#### age group
			if P[i][10]in Age_Group_Dict.keys():
			 	P[i][3] =  Age_Group_Dict[P[i][10]]   ### set the age group based on the increasing age

			P[i][11]= P[i][11]+1

			######@@@@@@@@@@ life to death
			####### MAYBE GPU
			stratname=str(P[i][1]) + ' ' + str(P[i][3])  ### only has sex and age group as stratum name
			tpbase=float(LifeDeath_Stratum_dict[stratname]) ### get the risk value

			a=P[i][15:25]  ### risk factors
			b=[1.0,5.9,1.41,1.0,5.6,1.24,15.0,1.0,3.0,1.8]            ### risk factor adjustment for life to death
			adjustval=np.dot(a,b)
			if adjustval > 0 :
				tpbase=float(tpbase * adjustval)
				#print "Life to death ", tpbase,adjustval,tpadjust



			r=float(random.uniform(0.0,1.0))
			if r < tpbase:
				P[i][27]=0 ### this person is dead at this cycle
				Dead=Dead+1  ### increasing number of dead people in whole program


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
			P[i][28]=1
	return P


def first_cycle(P,TP_dict):
	#### ALL people going from 0 to (1,2,3,30) are only stratified and the stratified id =1

	S_matrix=np.zeros((len(P),5), dtype='float64')
	TP_matrix=np.zeros((len(P),5), dtype='float64')

	for i in xrange(len(P)):
		S=[]
		TProb=[]
		S.append(0)
		TProb.append(0.0)
		for j in (1,2,3,30): #### from 0 it only goes to these states

			#### staratum id =1 (lengthin us+_bp+sex+race+age group)
			stratname= str(P[i][5]) +  ' ' + str(P[i][6]) + ' '  + str(P[i][1]) +  ' ' + str(P[i][2]) +  ' ' + str(P[i][3])
			#print "First cycle ", i, P[i][8], j, stratname
			tpval=TP_dict[P[i][8],j][stratname]###get tp value by stratum name
			S.append(j)  ### add the next state and corresponding tp value in to list to be use later
			TProb.append(tpval)

		S_matrix[i]=S
		TP_matrix[i]=TProb

	row_sums = TP_matrix.sum(axis=1)
	TP_matrix = TP_matrix / row_sums[:, np.newaxis]



	for i in xrange(len(TP_matrix)):  ### maybe parallel
		sortinds=TP_matrix[i].argsort()  ## sorting T list and then sort S based on the sorted indices
		TP_matrix[i]=TP_matrix[i][sortinds]
		S_matrix[i]=S_matrix[i][sortinds]


	return S_matrix, TP_matrix
