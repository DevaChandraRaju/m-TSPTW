# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:34:30 2017

@author: Deva Chandra Raju Malla
"""
import numpy as np
import pandas as pd 
import os
import copy
from time import gmtime, strftime, time
from SpringClean_DataPull import pull_from_mySQL
from SpringClean_Genetic_Algorithm import Genetic_Algorithm

os.chdir('C:/Users/dt81540/Desktop/DataScience/Travelling Salesmen Problem - Project/ROS/')

### This is capture the start time
start = strftime("%Y-%m-%d %H:%M:%S", gmtime())
### This function is to pull spring_clean data from mySQL database
#parameters_df, stop_df, travel_df=pull_from_mySQL()
#print("parameters_df :",parameters_df)

parameters_df = pd.read_csv('parameters_info_db.csv',sep=',')
stop_df = pd.read_csv('stop_info_db.csv',sep=',')
travel_df = pd.read_csv('travel_time_matrix_db.csv',sep=',')
test_grid = pd.read_csv('penatly_test.csv',sep=',')

### converting dataframes into numpy array for row and column wise operations flexibility
parameters_info_db = np.array(parameters_df)
stop_info_db = np.array(stop_df)
travel_time_matrix_db = np.array(travel_df)
test_grid_np = np.array(test_grid)

stop_unique = np.sort(stop_info_db[:,0])

### Convert travel time matrix into multi dimentional array and also list all missing stops and corresponding indexes.
k = 0
j = 0
missing_stops_idx = []
missing_stops = []

## Converting travel time_matrix into 2D array
travel_time_MD = np.zeros(shape=[stop_info_db.shape[0],stop_info_db.shape[0]])
for i in range(stop_info_db.shape[0]):
    if stop_unique[i] == travel_time_matrix_db[k,0]:
        for l in range(stop_info_db.shape[0]):
            travel_time_MD[i,l] = travel_time_matrix_db[k,2]
            k = k + 1
    else:
        missing_stops_idx.append(i)
        missing_stops.append(stop_unique[i])
        

###### IMPORTANT NOTE -- This need to be modified ########
### this logic is to impute missing stops travel time with assumption that missing stops symmetric.
for i in missing_stops_idx:
    travel_time_MD[i,:] = travel_time_MD[:,i]

### dropping similar deopts related columns and rows from array
travel_time_MD_unq = np.delete(travel_time_MD, [4,5], 1) # Axis = 1 for Columnwise
travel_time_MD_unq = np.delete(travel_time_MD_unq, [4,5], 0) # axis = 0 for Row wise
stop_info_db_final = np.delete(stop_info_db, [4,5], 0) ## to delete duplicate depots

###### Genetic_Alogorithm Parameters ######
##Genetic_Algorithm(travel_dist_matrix, ==> two dimentional travel time matrix
##                 stop_service_info, ==> stops info database
##                 parameters_info,   ==> parameters info database
##                 stops_allowed,==> solution stops range: provide 0 for 3 to 5, 1 for 4 to 6 and 2 for 5 to 7
##                 iterations, ==> number of iteration to find a optimum solution
##                 mutate_per, ==> mutation percentage
##                 elite_per, ==> elite population percentage
##                 origPopSize): ==> size of population

### This logic process the test conditions from csv file and iterates genetic algorithm for different test conditions. 
optimized_route = []                 
f = open('bestRoutes_run_penalty.txt', 'w')
for test_iter in range(test_grid_np.shape[0]):
    
    print("###################### Test condition" , test_iter + 1 ,"processing started #######################")
    
    (h, m, s) = strftime("%H:%M:%S", gmtime()).split(':')
    test_start_time = int(h) * 3600 + int(m) * 60 + int(s)

    ### Genetic Alogorithm ####
    best_score, tot_vehicles, best_route, final_penalty  = Genetic_Algorithm(travel_time_MD_unq,
                                                              stop_info_db_final,
                                                              parameters_info_db,
                                                              int(test_grid_np[test_iter,1]),
                                                              int(test_grid_np[test_iter,2]),
                                                              test_grid_np[test_iter,3],
                                                              test_grid_np[test_iter,4],
                                                              int(test_grid_np[test_iter,5]))
    test_grid_np[test_iter,9] = best_score
    test_grid_np[test_iter,10] = tot_vehicles
    test_grid_np[test_iter,11] = np.sum(stop_info_db_final[:,1])
    test_grid_np[test_iter,12] = float((best_score * test_grid_np[test_iter,6]) + (test_grid_np[test_iter,10] * test_grid_np[test_iter,7])) 
    test_grid_np[test_iter,13] = float(test_grid_np[test_iter,11] * test_grid_np[test_iter,8])
    test_grid_np[test_iter,14] = final_penalty
    best_fit = copy.deepcopy(best_route[0:4])
    for i in range(len(best_fit)):
        for j in range(len(best_fit[i])):
            for k in range(len(best_fit[i][j])):
                best_fit[i][j][k] = stop_info_db_final[best_fit[i][j][k],0]
    
    print("Best Route -- ", best_fit)
    (h, m, s) = strftime("%H:%M:%S", gmtime()).split(':')
    test_end_time = int(h) * 3600 + int(m) * 60 + int(s)
    test_grid_np[test_iter,15] = (test_end_time - test_start_time)/60

    
    
    mystr = "Best Route from test condition : " + str(test_iter + 1) + "\n" + ', '.join([str(veh) for veh in best_fit]) + "\n" + "\n"
    f.write(mystr) 

f.close()

test_grid = pd.DataFrame(test_grid_np,columns=test_grid.columns)
test_grid.to_csv("penalty_test_results.csv")

print("Process Start Time :", start)
print("Process End Time   :", strftime("%Y-%m-%d %H:%M:%S", gmtime()))


#### Vehicle cost per mile = 0.8 $
#### per day cost of vehicle rent = 70 $
#### driver hourly wage = 18 $ or 0.3$ per minute




