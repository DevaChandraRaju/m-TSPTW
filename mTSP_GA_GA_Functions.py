# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:42:46 2017

@author: Deva Chandra Raju Malla
"""
import random
import numpy as np

### This is to generate chromosome(which combines routes of vechiles belongs to each depot). 
### This funtion returns a vehicle route in list of list of lists.

def generate_chromosome(depot_stops_array,Min_Veh,Max_Veh,depot_num):
    random.shuffle(depot_stops_array)  ## This is random shuffle stops assigned to depot.
    
    depot_vehs_route = []
    i = 0
    while i <= depot_stops_array.shape[0]:   
        stops_number = np.random.randint(Min_Veh,Max_Veh+1)
        
        veh_route = [depot_num]
        ## Below logic is to assign left over stops at the end of route to final vehicle. 
        if i + stops_number > (depot_stops_array.shape[0]): 
            stops_number = (depot_stops_array.shape[0] - i)
        
        if stops_number > 0:
            for _ in range(stops_number):
                i = i + 1
                veh_route.append(depot_stops_array[i-1])
            veh_route.append(depot_num)
            depot_vehs_route.append(veh_route)
        else:
            break
    return depot_vehs_route
    

### This function is to generate population from a shortest distance stops for each depot
def generate_population(pop_size,travel_time_depts,veh_limit_parms):
### Assigning a stops to each depot based on shotest distance. This logic uses argmin funtion to pull the index of shortest distance
    depot_stops = [[],[],[],[]]
    for i in range(travel_time_depts.shape[1]):
        depot_idx = np.argmin(travel_time_depts[:,i],0)
        depot_stops[depot_idx].append(i)
        
    InitPopulation = []
    for _ in range(pop_size):
        chromosome = []
        for dept in range(len(depot_stops)):
            stops_dept_np = np.array(depot_stops[dept][1:])
            veh_route = generate_chromosome(stops_dept_np,veh_limit_parms[1],veh_limit_parms[0],dept)
            chromosome.append(veh_route)
    
        InitPopulation.append(chromosome)
    return(InitPopulation)
    
### This function is to generate population from a random stops for each depot
def generate_population_rand(pop_size,travel_time_depts,veh_limit_parms):
    
    depot_stops = [[],[],[],[]]
    for i in range(travel_time_depts.shape[1]):
        depot_idx = np.random.randint(0,high=4,size=1)
        depot_stops[depot_idx[0]].append(i)
    
    InitPopulation = []
    for _ in range(pop_size):
        chromosome = []
        for dept in range(len(depot_stops)):
            stops_dept_np = np.array(depot_stops[dept][1:])
            veh_route = generate_chromosome(stops_dept_np,veh_limit_parms[1],veh_limit_parms[0],dept)
            chromosome.append(veh_route)
    
        InitPopulation.append(chromosome)
    return(InitPopulation)

## This function is to mutate the individuals - Approach is to swap vehicle routes across depots.
def mutate_across_depots(mutate_parent):
    ds = random.sample(range(len(mutate_parent)-2),2) ## This is to pick the two random depots to mutate
        
    # this is to pick the random vehicle under ramdomly selected depot.
    vh1 = random.sample(range(len(mutate_parent[ds[0]])-1),1)
    vh2 = random.sample(range(len(mutate_parent[ds[1]])-1),1)
    
    depot1 = mutate_parent[ds[0]][vh1[0]][0]
    depot2 = mutate_parent[ds[1]][vh2[0]][0]

    mutate_parent[ds[0]][vh1[0]] = [x if x != depot1 else depot2 for x in mutate_parent[ds[0]][vh1[0]]]
    mutate_parent[ds[1]][vh2[0]] = [x if x != depot2 else depot1 for x in mutate_parent[ds[1]][vh2[0]]]

    ### Below is to swap (mutate routes of a vehicle   
    mutate_parent[ds[0]][vh1[0]], mutate_parent[ds[1]][vh2[0]] = mutate_parent[ds[1]][vh2[0]], mutate_parent[ds[0]][vh1[0]]
        
    mutate_parent[4] = 0
    
    return(mutate_parent)

## This function is to mutate the individuals - Approach is to swap stops within vehicle routes.
def mutate_within_route(mutate_parent):
    
    ds = random.sample(range(len(mutate_parent)-1),2) ## This is to pick the random two depots to mutate
        
    # this is to pick the random vehicle under ramdomly selected depot.
    vh1 = random.sample(range(len(mutate_parent[ds[0]])-1),1)
    vh2 = random.sample(range(len(mutate_parent[ds[1]])-1),1)
    
    # Select the stop randomly for each vehicle route -
    vh1_stop = np.random.randint(1,high=(len(mutate_parent[ds[0]][vh1[0]])-1),size=1)
    vh2_stop = np.random.randint(1,high=(len(mutate_parent[ds[1]][vh2[0]])-1),size=1)
    
    
    ### Below is to swap (mutate routes of a vehicle 
    mutate_parent[ds[0]][vh1[0]][1], mutate_parent[ds[0]][vh1[0]][vh1_stop[0]] = mutate_parent[ds[0]][vh1[0]][vh1_stop[0]], mutate_parent[ds[0]][vh1[0]][1]
    mutate_parent[ds[1]][vh2[0]][1], mutate_parent[ds[1]][vh2[0]][vh2_stop[0]] = mutate_parent[ds[1]][vh2[0]][vh2_stop[0]], mutate_parent[ds[1]][vh2[0]][1]
    
    mutate_parent[4] = 0
    
    return(mutate_parent)
    
def crossOver(parent1,parent2):
## produce two childerns using from parent 1 and parent 2
    child = [parent1]
    child.append(parent2)
    
    number_of_stops = 189
    depots_nums = [0,1,2,3]
    
    for i in range(len(child)):
        if i == 0:
            l = child[i+1][0:4]
        elif i == 1:
            l = child[i-1][0:4]
        else:
            print("Out of Boundary - This CrossOver funtion capable to generate two childs from parents")
        
        unsaved_gene = []
        stops_random = random.sample(range(4,number_of_stops+5),number_of_stops - round(number_of_stops * 0.5))
        flatten = lambda l: [item for depots in l for vehicles in depots for item in vehicles]
        
        parent_f = flatten(l)
        for k in range(len(parent_f)): 
            if ((parent_f[k] in stops_random) or 
                (parent_f[k] in depots_nums)):
                pass
            elif parent_f[k] not in depots_nums:
                unsaved_gene.append(parent_f[k])    
    
        j = 0
        for depots in range(len(child[i])-2):
            for vehs in range(len(child[i][depots])):
                for stop in range(len(child[i][depots][vehs])):
                    if ((child[i][depots][vehs][stop] in stops_random) or 
                        (child[i][depots][vehs][stop] in depots_nums)):
                        pass
                    elif child[i][depots][vehs][stop] not in depots_nums:
                        child[i][depots][vehs][stop] = unsaved_gene[j]
                        j = j + 1  
        child[i][4] = 0 # reset the time calculated to re-calculate for child
        
    return(child) 