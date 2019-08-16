############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Cuckoo Search

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Cuckoo_Search, File: Python-MH-Cuckoo Search.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Cuckoo_Search>

############################################################################

# Required Libraries
import numpy  as np
import math
import random
import os

# Function
def target_function():
    return

# Function: Initialize Variables
def initial_position(birds = 3, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    position = np.zeros((birds, len(min_values) + 1))
    for i in range(0, birds):
        for j in range(0, len(min_values)):
             position[i,j] = random.uniform(min_values[j], max_values[j])
        position[i,-1] = target_function(position[i,0:position.shape[1]-1])
    return position

# Function: Levy Distribution
def levy_flight(mean):
	x1 = math.sin((mean - 1.0)*(random.uniform(-0.5*math.pi, 0.5*math.pi)) )/(math.pow(math.cos((random.uniform(-0.5*math.pi, 0.5*math.pi))), (1.0/(mean - 1.0))))
	x2 = math.pow((math.cos((2.0 - mean)*(random.uniform(-0.5*math.pi, 0.5*math.pi)))/(-math.log(random.uniform(0.0, 1.0)))), ((2.0 - mean)/(mean - 1.0)))
	return x1*x2

# Function: Replace Bird
def replace_bird(position, alpha_value = 0.01, lambda_value = 1.5, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    random_bird  = np.random.randint(position.shape[0], size = 1)[0]
    new_solution = np.zeros((1, position.shape[1]))  
    for j in range(0, position.shape[1] - 1):
        new_solution[0, j] = np.clip(position[random_bird, j] + alpha_value*levy_flight(lambda_value)*position[random_bird, j]*(int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)), min_values[j], max_values[j])
    new_solution[0,-1] = target_function(new_solution[0,0:new_solution.shape[1]-1])
    if (position[random_bird, -1] > new_solution[0,-1]):
        position[random_bird, j] = np.copy(new_solution[0, j])
    return position

# Function: Update Positions
def update_positions(position, discovery_rate = 0.25, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    updated_position = np.copy(position)
    abandoned_nests  = math.ceil(discovery_rate*updated_position.shape[0]) + 1
    random_bird_j    = np.random.randint(position.shape[0], size = 1)[0]
    random_bird_k    = np.random.randint(position.shape[0], size = 1)[0]
    while(random_bird_j == random_bird_k):
        random_bird_j = np.random.randint(position.shape[0], size = 1)[0]
    nest_list = list(position.argsort()[-(abandoned_nests-1):][::-1][0])
    for i in range(0, updated_position.shape[0]):
        for j in range(0, len(nest_list)):
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            if(i == nest_list[j] and rand > discovery_rate):
                for k in range(0, updated_position.shape[1] - 1):
                    rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                    updated_position[i,k] = np.clip(updated_position[i,k]  + rand*(updated_position[random_bird_j,k] - updated_position[random_bird_k,k]), min_values[k], max_values[k])
        updated_position[i,-1] = target_function(updated_position[i,0:updated_position.shape[1]-1])          
    return updated_position

# CS Function
def cuckoo_search(birds = 3, discovery_rate = 0.25, alpha_value = 0.01, lambda_value = 1.5, min_values = [-5,-5], max_values = [5,5], iterations = 50, target_function = target_function):    
    count = 0
    position = initial_position(birds = birds, min_values = min_values, max_values = max_values, target_function = target_function)    
    best_ind = np.copy(position[position[:,-1].argsort()][0,:])
    while (count <= iterations):
        print("Iteration = ", count, " of ", iterations, " f(x) = ", best_ind[-1])    
        for i in range(0, position.shape[0]):
            position = replace_bird(position, alpha_value = alpha_value, lambda_value = lambda_value, min_values = min_values, max_values = max_values, target_function = target_function)
        position = update_positions(position, discovery_rate = discovery_rate, min_values = min_values, max_values = max_values, target_function = target_function)
        value = np.copy(position[position[:,-1].argsort()][0,:]) 
        if (best_ind[-1] > value[-1]):
            best_ind = np.copy(position[position[:,-1].argsort()][0,:])     
        count = count + 1 
    print(best_ind)    
    return best_ind

######################## Part 1 - Usage ####################################

# Function to be Minimized (Six Hump Camel Back). Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def six_hump_camel_back(variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

cs = cuckoo_search(birds = 500, discovery_rate = 0.25, alpha_value = 0.01, lambda_value = 1.5, min_values = [-5,-5], max_values = [5,5], iterations = 1000, target_function = six_hump_camel_back)

# Function to be Minimized (Rosenbrocks Valley). Solution ->  f(x) = 0; xi = 1
def rosenbrocks_valley(variables_values = [0,0]):
    func_value = 0
    last_x = variables_values[0]
    for i in range(1, len(variables_values)):
        func_value = func_value + (100 * math.pow((variables_values[i] - math.pow(last_x, 2)), 2)) + math.pow(1 - last_x, 2)
    return func_value

cs = cuckoo_search(birds = 1000, discovery_rate = 0.02, alpha_value = 0.15, lambda_value = 1.5, min_values = [-5,-5], max_values = [5,5], iterations = 100, target_function = rosenbrocks_valley)

