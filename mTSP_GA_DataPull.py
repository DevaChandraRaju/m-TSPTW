# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:00:15 2017

@author: Deva Chandra Raju Malla
"""
import pymysql.cursors

def pull_from_mySQL():
#### For mysql connectivity

#### Connect to mysql using the appropriate credentials to the desired database.

    connection = pymysql.connect(host='ip-172-31-13-154',
                                 user='insofeadmin',
                                 password='MDQzZTgyYj',
                                 db='insofe_1047_spring_clean',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
### Extract data from active_emp_details table

            query = "SELECT * FROM `parameters_info_db`"
            cursor.execute(query)
            parameters_db = cursor.fetchall()

### Extract data from dept_aggr_by_gender table
            query = "SELECT * FROM `stops_info_db`"
            cursor.execute(query)
            stops_db = cursor.fetchall()

### Extract data from dept_aggr table
            query = "SELECT * FROM `travel_time_matrix_db`"
            cursor.execute(query)
            travel_time_db = cursor.fetchall()
        #print(dept_aggr_all)
        
    finally:
        connection.close()
            
    return(parameters_db,stops_db,travel_time_db)
    
