
import re
import copy
import random
import collections
import scipy.io
import numpy as np
import networkx as nx
from tqdm import tqdm
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

import SmallestCycles
from SmallestCycles import *
import DC_function
from DC_function import *

# SIR model
def sir_model(G, status, transmission_rate, recovery_rate, max_steps=100):
    infected_nodes = [i for i, s in enumerate(status) if s == "I"]
    susceptible_nodes = [i for i, s in enumerate(status) if s == "S"]
    recovered_nodes = []

    susceptible_counts = [len(susceptible_nodes)]
    infected_counts = [len(infected_nodes)]
    recovered_counts = [0]

    for step in range(max_steps):
        # spread process
        for infected_node in infected_nodes:
            neighbors = G.neighbors(infected_node)
            for neighbor in neighbors:
                if status[neighbor] == "S" and np.random.rand() < transmission_rate:
                    status[neighbor] = "I"

        # recovery process
        for infected_node in infected_nodes:
            if np.random.rand() < recovery_rate:
                status[infected_node] = "R"
                recovered_nodes.append(infected_node)

        # Update the list of infected and susceptible nodes
        infected_nodes = [i for i, s in enumerate(status) if s == "I"]
        susceptible_nodes = [i for i, s in enumerate(status) if s == "S"]
        recovered_counts.append(len(recovered_nodes))
        susceptible_counts.append(len(susceptible_nodes))
        infected_counts.append(len(infected_nodes))

        # If there are no infected nodes, end the simulation
        if len(infected_nodes) == 0:
            break

    return susceptible_counts, infected_counts, recovered_counts


NetworkAddress = r'Email.txt'
networkName = 'Email'
Mygraph = nx.Graph()
rawC = 0
file = open(NetworkAddress)
while 1:
    lines = file.readlines(10000)
    if not lines:
        break
    for line in lines:
        #input format of the network
        line = line[:-1]
        Mygraph.add_edge(int(line[:6]), int(line[7:]))
file.close()
NodeNum = Mygraph.number_of_nodes()  
N = Mygraph.number_of_nodes()  
Mygraph.remove_edges_from(nx.selfloop_edges(Mygraph))


# Define infection rate and recovery rate
degrees = Mygraph.degree()
average_degree = sum(degree for node, degree in degrees) / len(Mygraph.nodes())
degree_squares = [degree ** 2 for node, degree in degrees]
average_squared_degree = sum(degree_squares) / len(Mygraph.nodes())
transmission_rate = average_degree / (average_squared_degree - average_degree)
recovery_rate = 1

sorted_nodes_deg=node_degree(Mygraph)
SmallestCycles = get_smallest_cycles(Mygraph)
sorted_cycles_degree, sorted_cycles_ratio=cyclesFeature(Mygraph, SmallestCycles)

a = 0.8
deg_dict = dict(sorted_nodes_deg)
new_list = []
for node, value in sorted_cycles_ratio:
    new_value = a * deg_dict[node] + (1 - a) * value
    new_list.append((node, new_value))
weighted_list = sorted(new_list, key=lambda x: x[1], reverse=True) 

sorted_nodes_cycles_ratio = []
for t in weighted_list:
    sorted_nodes_cycles_ratio.append(t[0])

k = int((len(Mygraph.nodes()))*0.1)
top_k = sorted_nodes_cycles_ratio[:k]

# Initialize node status
status = ["S"] * len(Mygraph.nodes())
for node_index in top_k:
    status[node_index] = "I"

R = []
Infections = []
times = 22   
infected_lists = []

for i in range(8000):
    status1 = copy.deepcopy(status)
    susceptible_counts, infected_counts, recovered_counts = sir_model(Mygraph, status1, transmission_rate, recovery_rate)

    if len(infected_counts) > times:
        infected_lists.append(infected_counts[:times])
    else:
        infected_counts.extend([infected_counts[-1]] * (times - len(infected_counts)))
        infected_lists.append(infected_counts)  

average_infected_counts = []
for i in range(len(infected_lists[0])):
    values_at_step_i = [lst[i] for lst in infected_lists]
    average_infected_counts.append(np.mean(values_at_step_i))
    
    R.append(sum(average_infected_counts))

R = [elem - k for elem in R]
R = [round(x, 1) for x in R]
print("List of Cumulative Infected Groups:", R[-(times-1):])

