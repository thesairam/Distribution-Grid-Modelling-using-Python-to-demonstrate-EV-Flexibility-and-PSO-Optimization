# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 13:22:12 2022

@author: alank
"""
import time
import numpy as np
#import pandas as pd

import random as rd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt
#import seaborn as sns
time_axis=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
I_load = np.multiply([0,1.632, 1.525 ,1.454, 2.021 ,2.567, 1.454, 2.021, 1.345, 1.654, 1.456, 1.245 ,1.145, 1.000 ,0.350],500)   
print(I_load)
# cost function
def cost(I_DM,I_EV,h_d):
    for k in range(h_d):
        Loss = np.square(I_DM[k]+sum(I_EV[:,k]))
    return Loss

# soc of ev
def SOC_to_I_EV(X_i):
     C = 1  
     I_EV = np.zeros_like(X_i)
     for k in range(1,len(X_i)):
         I_EV[k] = (X_i[k]-X_i[k-1])*C/1
     return I_EV

# constraint     
def constraint(X,E_req,Ecap,mini,maxi):
     [n,m]=X.shape
     con = np.zeros((n,m-1))
     for j in range(n):
         if np.all(X<=100):
             if (E_req[j] >= mini) and (E_req[j] <= maxi):
                 if X[j,-1] >= E_req[j]:
                     for k in range(m-1):
                         if np.absolute(X[j,k]-X[j,k+1]) <= Ecap:
                             con[j,k]=1
     if np.all(con == 1): 
         constraint = 1
     else:
         constraint = 0
     return constraint

# gbest update
def FindBestSolution(X,fit):
    min_fit = min(fit)
    a = np.argmin(fit)
    gbest = X[a];
    return gbest, min_fit

# pbest update
def FindBetterSolution(pbest,pbest_fit,pos,fit):
    if pbest_fit < fit:
       return pbest, pbest_fit
    else:
        return pos, fit

#PSO optimisation
def Pso(N_EV,Ecap,par_Num,IterNum):
    start = time.process_time()
    # weights
    w = 0.4
    c1 = 2
    c2 = 2
    i = 0 
    # EV parameters
    h_d = 14                                              # MAX E change in percentage of soc
    mini = 20
    maxi = 100
    # PSO parameters
    X = np.empty((par_Num,N_EV,h_d+1))
    X_mid = np.empty((N_EV,h_d+1))
                                                   # Charging C value
    pbest = np.empty((par_Num,N_EV,h_d+1))
    pbest_fit = np.empty(par_Num)
    
    I_EV_i = np.zeros_like(X)
    
    fit = np.zeros(par_Num)
    E_req = np.random.randint(75,95,(N_EV,1))               # Minimum end soc required
    
    # timer
  
    msur1 = time.process_time() - start
    print('Initilization time:', msur1)
    nloop = 0
    # X_a =  np.random.randint(20,21,(N_EV,1))     
    while i < par_Num:
        X_a = np.random.randint(20,40,(N_EV,1))
        for m in range(N_EV):
            X_mid[m,0] = X_a[m]+rd.randint(-Ecap,Ecap+1)
            for n in range(1,h_d+1):
                polygon = Polygon([(0,X_a[m]), (0, mini), ((mini-E_req[m])/Ecap+h_d, mini), (h_d, E_req[m]),(h_d,maxi),((maxi-X_a[m])/Ecap,maxi)])
                point=Point(0,0)
                while polygon.covers(point)== False:
                    k=np.random.randint(-Ecap,Ecap+1)
                    X_mid[m,n] = X_mid[m,n-1]+k
                    point = Point(n, X_mid[m,n])  
        pos = X_mid
        X[i] = pos
        for j in range(pos.shape[0]):
            I_EV_i[i,j] = SOC_to_I_EV(pos[j,:])
        fit[i] = cost(I_load,I_EV_i[i],h_d)
        const = constraint(pos,E_req,Ecap,mini,maxi)
        nloop = nloop+1
        if const == 1:
            pbest[i] = pos 
            pbest_fit[i] = fit[i]
            i = i+1        
            print(i, nloop)
            nloop = 0
                    
    gbest, gbest_fit = FindBestSolution(pbest,pbest_fit)
    gbest_before_opt=gbest
    #print(gbest)
    # print('The value of gbest fit:', gbest_fit)
    
    # timer
    msur2 = time.process_time() - msur1
    print('Input randomization time:', msur2)
    
    # velocity update (iterations)
    Vel = np.zeros((par_Num,N_EV,h_d+1))
    for k in range(IterNum):
        for i in range(par_Num):
            Vel[i] = w*Vel[i] + c1*np.random.rand()*(pbest[i]-X[i]) + c2*np.random.rand()*(gbest-X[i])
            pos = X[i] + Vel[i]
            X[i] = pos
            for j in range(pos.shape[0]):
                I_EV_i[i,j] = SOC_to_I_EV(pos[j,:])
            fit[i] = cost(I_load,I_EV_i[i],h_d)
            const = constraint(pos,E_req,Ecap,mini,maxi)
            if const==1:
                pbest[i], pbest_fit[i] = FindBetterSolution(pbest[i],pbest_fit[i],X[i],fit[i])
                 
    gbest, gbest_fit = FindBestSolution(pbest,pbest_fit)  
  
    # print('The value of gbest fit:', gbest_fit)
    
    # timer
    msur3 = time.process_time() - msur2
    print('PSO Iteration time:', msur3)
    return gbest,gbest_fit,gbest_before_opt,msur2+msur3
    
    #Plot SOC for EVs
    # nEVs = 4                                    # Plot first nEVs
    # df_gbest = pd.DataFrame(gbest[:nEVs,:])
    # df_gbest.T.plot.line()                      
    
    # Comments
    # 1. X_mid initilization is extremely slow
    # 2. Included time function and nloop to see the number 
    # of iterations it takes for you to get a random series abiding the constraints
    # 3. PSO is actually fast just initilization issues
    
# main results#

# data=[]
# for N_EV in range(10,110,10):
#     for par_Num in range(20,110,20):

gbest1,gbest_fit1,gbest_before_opt,T=Pso(200,20,100,1000)
print(T)

        # I_EV_best=np.zeros_like(gbest1)
        # for j in range(gbest1.shape[0]):
        #     I_EV_best[j] = SOC_to_I_EV(gbest1[j,:])
        
        # I_EV_best = np.sum(I_EV_best,axis=0)
        
        
        # data.append([N_EV,par_Num,T])
        # plt.plot(time_axis,gbest1[0,:].T,color='green', linestyle='-', label="after optimisation")
        # plt.plot(time_axis,gbest1[1,:].T,color='red', linestyle='-')
        # plt.plot(time_axis,gbest1[2,:].T,color='blue', linestyle='-')
        # plt.plot(time_axis,gbest_before_opt[0,:].T,color='green', linestyle='--',label='before optimisation')
        # plt.plot(time_axis,gbest_before_opt[1,:].T,color='red', linestyle='--')
        # plt.plot(time_axis,gbest_before_opt[2,:].T,color='blue', linestyle='--')
        # plt.xlabel("time")
        # plt.ylabel("SOC(%)")
        # plt.legend(loc="upper left")
        # plt.xticks(ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],labels=[18,19,20,21,22,23,24,1,2,3,4,5,6,7,8])
        
        # plt.show()
# plt.bar(time_axis,I_EV_best.T,color='green', linestyle='-', label="EV demand")

# plt.plot(time_axis,I_load.T,color='red', linestyle='-',label='Residential demand')
# plt.xlabel("time")
# plt.ylabel("I_EV")
# plt.legend(loc="upper left")
# plt.xticks(ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],labels=[18,19,20,21,22,23,24,1,2,3,4,5,6,7,8])

# plt.show()

# print(data)
        
    
