# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:34:30 2017

@author: Deva Chandra Raju Malla
"""

### This fucntion is to calculate the time taken(fitness) by each vehicle
def fitness_calc(population,travel_dist_matrix,stop_service_info,service_time_window,penalty_time_window):
    population_temp = population
    for i in range(len(population)):
        chromosome_total, tot_penatly = 0, 0
        for j in range(len(population[i])):
            Depot_travel_time = 0
            for k in range(len(population[i][j])):
                vehicle_route = population[i][j][k]
                ##### Vechile route time funtion to calculate the route times between each stop #######
                Vehicle_travel_time, penalty_only = vechile_route_time(vehicle_route,travel_dist_matrix,stop_service_info,penalty_time_window)
                
                Depot_travel_time = Depot_travel_time + Vehicle_travel_time
                tot_penatly = penalty_only + tot_penatly
            chromosome_total = chromosome_total + Depot_travel_time
        population_temp[i].append(round(chromosome_total,1))
        population_temp[i].append(round(tot_penatly,1))
        
    return(population_temp)


### this function is to calculate vehicle time and checks penatly constraints for each vehicle route
def vechile_route_time(vehicle_route,travel_dist_matrix,stop_service_info,penalty_time_window):
    total_penalty_time, total_penalty_percent, penalty_time, penalty_percent = 0, 0, 0, 0
    stops_count = len(vehicle_route) - 2 # substracting first and last depot count from stops count

    ## Calculates the stops threshold penalty
    penalty_time, penalty_percent =  penalty_cal_slab_basis(2,penalty_time_window,stops_count,' ',0,0)
    total_penalty_time = total_penalty_time + penalty_time
    total_penalty_percent = total_penalty_percent + penalty_percent
    
    Vehicle_travel_time, reach_time = 0, 0
    penalty_time, penalty_percent = 0, 0
    
    for l in range(len(vehicle_route)):
        if l > 0:
            from_stop = vehicle_route[l-1]
            to_stop = vehicle_route[l]
            Vehicle_travel_time = Vehicle_travel_time + travel_dist_matrix[from_stop,to_stop] + stop_service_info[to_stop,1]
            reach_time = reach_time + stop_service_info[to_stop,1]
            
            if l > 1:
                reach_time = reach_time + travel_dist_matrix[from_stop,to_stop]
            
    # Calculates the penatly at every stop based on the reach time and allowed time window
    penalty_time, penalty_percent =  penalty_cal_slab_basis(3,penalty_time_window,0,stop_service_info[to_stop,:],reach_time,0)
    total_penalty_time = total_penalty_time + penalty_time
    total_penalty_percent = total_penalty_percent + penalty_percent
            
    penalty_time, penalty_percent =  penalty_cal_slab_basis(1,penalty_time_window,0,'',0,Vehicle_travel_time)
    total_penalty_time = total_penalty_time + penalty_time
    total_penalty_percent = total_penalty_percent + penalty_percent
    
    only_penalty = total_penalty_time + (total_penalty_percent * Vehicle_travel_time)
      
    total_route_time_with_penalty = Vehicle_travel_time + only_penalty
    
    return(total_route_time_with_penalty, only_penalty)

### this function is to calculate vehicle time and checks penatly constraints at every stop.
def vechile_route_time_2(vehicle_route,travel_dist_matrix,stop_service_info,penalty_time_window):
    total_penalty_time, total_penalty_percent, penalty_time, penalty_percent = 0, 0, 0, 0
    stops_count = len(vehicle_route) - 2 # substracting first and last depot count from stops count
    ### Calculate the stops threshold penalty
    penalty_time, penalty_percent =  penalty_cal_slab_basis(2,penalty_time_window,stops_count,' ',0,0)
    total_penalty_time = total_penalty_time + penalty_time
    total_penalty_percent = total_penalty_percent + penalty_percent
    
    Vehicle_travel_time, reach_time = 0, 0
    penalty_time, penalty_percent = 0, 0
    
    for l in range(len(vehicle_route)):
        if l > 0:
            from_stop = vehicle_route[l-1]
            to_stop = vehicle_route[l]
            Vehicle_travel_time = Vehicle_travel_time + travel_dist_matrix[from_stop,to_stop] + stop_service_info[to_stop,1]
            reach_time = reach_time + stop_service_info[to_stop,1]
            
            if l > 1:
                reach_time = reach_time + travel_dist_matrix[from_stop,to_stop]
            
            # Calculates the penatly at every stop based on the reach time and allowed time window
            penalty_time, penalty_percent =  penalty_cal_slab_basis(3,penalty_time_window,0,stop_service_info[to_stop,:],reach_time,0)
            total_penalty_time = total_penalty_time + penalty_time
            total_penalty_percent = total_penalty_percent + penalty_percent
            
    penalty_time, penalty_percent =  penalty_cal_slab_basis(1,penalty_time_window,0,'',0,Vehicle_travel_time)
    total_penalty_time = total_penalty_time + penalty_time
    total_penalty_percent = total_penalty_percent + penalty_percent
    
    only_penalty = total_penalty_time + (total_penalty_percent * Vehicle_travel_time)
      
    total_route_time_with_penalty = Vehicle_travel_time + only_penalty
    
    return(total_route_time_with_penalty, only_penalty)



## This funtion takes the penalty type and returns the penalty time and percentage of penalty on total route time for a vehicle
## penalty_type catogerized into three to calculate the penalty: 
## 1 - total travel time penalty, 2  - stops threshold, 3 - before/after defined service window
## This function works for customer with different time windows as well.(Not only for time window i.e. 11:00 AM to 14:00 PM) 

################ Calculate penalty whenever below constraints are not met ###############################################
##
## ###### NOTE : Not considered below penalty as slab based.. Applied direct.
## 1.  Total travel and job execution must not exceed 660mins for any route. 
##    Apply penalty if exceeds, 
##        1 - 60 mins - exceeded minutes + 10% of total route time
##        61 - 120 mins - 2 times the exceeded minutes + 20% of total route time
##        121 - 180 mins - 3 times the exceeded minutes + 30% of total route time
##        181 - 240 mins - 4 times the exceeded minutes + 40% of total route time ...
##        
## 2. If any route has more/less than the stops threshold
##        1 stop - 10% of total route time
##        2 stops - 20% of total route time
##        3 stops - 30% of total route time...
##        
## 3. If a vehicle reaches a customer before/after small time window (30 mins) - no penalty
##   with in small and large time window - 10% of total route time
##   beyond large time window 
##        1st 60mins - exceeded minutes + 10% of total route time
##        2nd 60mins - 2 times the exceeded minutes + 20% of total route time
##
###########################################################################################################################

### Function to apply penatly at slab basis if contrainsts are not met.
def penalty_cal_slab_basis(penalty_type,penalty_parameters,stops_count,stop_service_info,reach_time,total_travel_time):
    
    penalty_time, penalty_mul_factor, penalty_percent = 0,0,0
    
    if penalty_type == 2: ## this is to check for stops threshold
        if (stops_count > penalty_parameters[0]):
            penalty_percent = stops_count - penalty_parameters[0]
            penalty_percent = penalty_percent * 0.1
        elif (stops_count < penalty_parameters[1]):
            penalty_percent = penalty_parameters[1] - stops_count
            penalty_percent = penalty_percent * 0.1
    
    elif penalty_type == 3: ## penalty before/after defined service window
        ## This is convert service time into minutes for comparion purpose
        (h, m, s) = stop_service_info[2].split(':')
        time1 = int(h) * 3600 + int(m) * 60 + int(s)
        (h, m, s) = stop_service_info[3].split(':')
        time2 = int(h) * 3600 + int(m) * 60 + int(s)
        allowed_time = (time2 - time1)/60
        
        ## Add no penalty window to timediff
        allowed_time = allowed_time + penalty_parameters[3]
        if reach_time > allowed_time:
            penalty_mul_factor = int((reach_time - allowed_time)/60) + 1
            time_diff = reach_time - allowed_time
            for i in range(1,penalty_mul_factor+1):
                slab_check = time_diff - (60 * i)
                if slab_check < 0:
                    penalty_time = penalty_time + (i * (time_diff - (60 * (i-1))))
                    penalty_percent = penalty_percent + round(0.1 * i,2)
                else:
                    penalty_time = penalty_time + ( i * 60 )
                    penalty_percent = penalty_percent + round(0.1 * i,2)
            
    elif penalty_type == 1: ## total travel time penalty
        if total_travel_time > penalty_parameters[2]:
            penalty_mul_factor = int((total_travel_time - penalty_parameters[2]) /60) + 1
            time_diff = total_travel_time - penalty_parameters[2]
            for i in range(1,penalty_mul_factor+1):
                slab_check = time_diff - (60 * i)
                if slab_check < 0:
                    penalty_time = penalty_time + (i * (time_diff - (60 * (i-1))))
                    penalty_percent = penalty_percent + round(0.1 * i,2)
                else:
                    penalty_time = penalty_time + ( i * 60 )
                    penalty_percent = penalty_percent + round(0.1 * i,2)            
        
    return(penalty_time,penalty_percent)

    
    
### Function to apply direct penatly on overrall time travelled.
def penalty_percent_calc(penalty_type,penalty_parameters,stops_count,stop_service_info,reach_time,total_travel_time):
    penalty_time, penalty_mul_factor, penalty_percent = 0,0,0
    
    if penalty_type == 2: ## this is to check for stops threshold
        if (stops_count > penalty_parameters[0]):
            penalty_percent = stops_count - penalty_parameters[0]
            penalty_percent = penalty_percent * 0.1
        elif (stops_count < penalty_parameters[1]):
            penalty_percent = penalty_parameters[1] - stops_count
            penalty_percent = penalty_percent * 0.1
    
    elif penalty_type == 3: ## penalty before/after defined service window
        ## This is convert service time into minutes for comparion purpose
        (h, m, s) = stop_service_info[2].split(':')
        time1 = int(h) * 3600 + int(m) * 60 + int(s)
        (h, m, s) = stop_service_info[3].split(':')
        time2 = int(h) * 3600 + int(m) * 60 + int(s)
        timediff = (time2 - time1)/60
        
        ## Add no penalty window to timediff
        timediff = timediff + penalty_parameters[3]
        if reach_time > timediff:
            penalty_mul_factor = int((reach_time - timediff)/60) + 1
            penalty_time = penalty_mul_factor * (reach_time - timediff)
            penalty_percent = round(0.1 * penalty_mul_factor,2)
            
    elif penalty_type == 1: ## total travel time penalty
        if total_travel_time > penalty_parameters[2]:
            penalty_mul_factor = int((total_travel_time - penalty_parameters[2]) /60) + 1
            penalty_time = penalty_mul_factor * (total_travel_time - penalty_parameters[2])
            penalty_percent = 0.1 * penalty_mul_factor
        
    return(penalty_time,penalty_percent)

