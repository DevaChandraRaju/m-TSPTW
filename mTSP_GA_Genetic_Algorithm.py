# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:51:00 2017

@author: Deva Chandra Raju Malla
"""
import numpy as np
import copy
import random
from SpringClean_GA_Functions import *
from SpringClean_TravelTime import fitness_calc

def Genetic_Algorithm(travel_dist_matrix,stop_service_info,parameters_info,veh_range,iterations,mutate_per,elite_per,origPopSize):
      
    service_time_window = parameters_info[veh_range,:] 
    penalty_time_window = parameters_info[veh_range+3,:]
### Pull only four depots from array to allocate stops to each depot
    stops_depots = travel_dist_matrix[:4,]

    ## Generating chrosome and population from clustered stops.
    InitPopulation = generate_population(origPopSize,stops_depots,service_time_window)
    
    ## Generating chromosome and population with randome depot and stop selection
    #InitPopulation = generate_population_rand(origPopSize,stops_depots,service_time_window)
    
    chomosome_time = fitness_calc(InitPopulation,travel_dist_matrix,stop_service_info,service_time_window,penalty_time_window)

## This logic is to sort population based on fitness
    chomosome_time = np.array(chomosome_time)
    srt = np.argsort(chomosome_time[:,4])
    InitPopulation = chomosome_time[srt,:]

    topElite=int(round(elite_per*origPopSize,0))
    population = InitPopulation[:topElite,]

    prev_best_score, loop_break_counter = 0, 0
    for iter in range(iterations):
        population = copy.deepcopy(population[:topElite,]) #deepcopy is to copy only content not reference of an object
    
        mutate = mutate_per/(iter + 1)
        

        while len(population) < origPopSize:  
            if (np.random.random_sample(1) < mutate):
                random_chromosome = np.random.randint(0,high=topElite,size=1)
                mutate_chromosome = copy.deepcopy(population[random_chromosome[0]])
            
                ### Random number to select mutation either across depots or within vehicle route
                mutated = mutate_across_depots(mutate_chromosome)
                #mutate_select = np.random.randint(0,high=2,size=1) 
                #if mutate_select == 0:
                #    mutated = mutate_across_depots(mutate_chromosome)
                #else:
                #    #mutated = mutate_within_route(mutate_chromosome)
                #    mutated = mutate_across_depots(mutate_chromosome)
                    
                mutate_ind = []
                mutate_ind.append(copy.deepcopy(mutated[:4].tolist()))
                chomosome_time = fitness_calc(mutate_ind,travel_dist_matrix,stop_service_info,service_time_window,penalty_time_window)
            else:
                cross_over_parents = random.sample(range(int(topElite)-1),2)
                parent_1 = copy.deepcopy(population[cross_over_parents[0]])
                parent_2 = copy.deepcopy(population[cross_over_parents[1]])
                childs = crossOver(parent_1,parent_2)
                childs = copy.deepcopy(np.array(childs)[:,:4].tolist())
                chomosome_time = fitness_calc(childs,travel_dist_matrix,stop_service_info,service_time_window,penalty_time_window)
        
            chomosome_time = np.array(chomosome_time)
            population = np.vstack([population,chomosome_time])
    
        srt = np.argsort(population[:,4])     
        population = population[srt,:]
        Tot_Vehicles = len(population[0][0])+len(population[0][1])+len(population[0][2])+len(population[0][3])
   
        #print("Best fitness score in iteration", iter, "=",(population[0][4]-population[0][5]), Tot_Vehicles, population[0][5])
        
        # Criteria to stop processing if route time is not converging for the last 100 iterations
        if prev_best_score == population[0][4]:
            loop_break_counter = loop_break_counter + 1
        else:
            loop_break_counter = 0
        prev_best_score = copy.deepcopy(population[0][4])
        
        if loop_break_counter > 100:
            print("### Information : At",iter,"algorithm not converged for last 100 iterations ### ") 
            break;
        
    print("Best fitness Score ", population[0][4])
    print("Penalty Applied ", population[0][5])
    print("Mutate Probability ", mutate_per)
    print("Iterations ", iterations)
    print("origPopSize ", origPopSize)
    print("Total # of vehicles :",Tot_Vehicles)
    
    return population[0][4],Tot_Vehicles,population[0],population[0][5]