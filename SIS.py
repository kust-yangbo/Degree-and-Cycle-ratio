
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

# SIS model
def sis_model(G, status, transmission_rate, recovery_rate, max_steps=100):
    N = G.number_of_nodes()  
    susceptible_nodes = [i for i, s in enumerate(status) if s == "S"]
    infected_nodes = [i for i, s in enumerate(status) if s == "I"]

    susceptible_counts = [len(susceptible_nodes)]
    infected_counts = [len(infected_nodes)]

    for step in range(max_steps):
        
        new_infected_nodes = []
        for infected_node in infected_nodes:
            for neighbor in G.neighbors(infected_node):
                if status[neighbor] == "S" and np.random.rand() < transmission_rate:
                    new_infected_nodes.append(neighbor)

        new_susceptible_nodes = []
        for infected_node in infected_nodes:
            if np.random.rand() < recovery_rate:
                new_susceptible_nodes.append(infected_node)

        for node in new_infected_nodes:
            status[node] = "I"
        for node in new_susceptible_nodes:
            status[node] = "S"

        infected_nodes = [i for i, s in enumerate(status) if s == "I"]
        susceptible_nodes = [i for i, s in enumerate(status) if s == "S"]
        susceptible_counts.append(len(susceptible_nodes))
        infected_counts.append(len(infected_nodes))

    return susceptible_counts, infected_counts



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
NodeNum = Mygraph.number_of_nodes()  #
N = Mygraph.number_of_nodes()  #
Mygraph.remove_edges_from(nx.selfloop_edges(Mygraph))


beta = 0.25  # infection rate
gamma = 0.5    # Recovery rate
I_0 = int(N/2)  # Initial infection count: Half of the nodes
S_0 = N-I_0     # Initial number of susceptible individuals
k=I_0
top_k_degrees = random.sample(list(Mygraph.nodes()), k)

# Initialize node status
status = ["S"] * len(Mygraph.nodes())
for node_index in top_k_degrees:
    status[node_index] = "I"    

infected_lists = []
susceptible_lists = []
for i in tqdm(range(1500)):
    status1 = copy.deepcopy(status)
    susceptible_counts, infected_counts = sis_model(Mygraph, status1, beta, gamma)
    infected_lists.append(infected_counts) 
    susceptible_lists.append(susceptible_counts) 

averages_infected_counts = []
for i in range(len(infected_lists[0])):  
    total = sum(list_i[i] for list_i in infected_lists)
    average = total / len(infected_lists)
    averages_infected_counts.append(average)

averages_susceptible_counts = []
for i in range(len(susceptible_lists[0])):  
    total = sum(list_i[i] for list_i in susceptible_lists)
    average = total / len(susceptible_lists)
    averages_susceptible_counts.append(average)

norm_averages_infected_counts = [x / N for x in averages_infected_counts]
norm_averages_susceptible_counts = [x / N for x in averages_susceptible_counts]

P = norm_averages_infected_counts[-20:]
P0 = sum(P)/len(P)
print('Steady state density without immunization P0:',P0)




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
NodeNum = Mygraph.number_of_nodes()  #
N = Mygraph.number_of_nodes()  #
Mygraph.remove_edges_from(nx.selfloop_edges(Mygraph))


sorted_nodes_deg=node_degree(Mygraph)
SmallestCycles = get_smallest_cycles(Mygraph)
sorted_cycles_degree, sorted_cycles_ratio=cyclesFeature(Mygraph, SmallestCycles)

my_list = list([0.28])
for j in my_list:
    a = j
    deg_dict = dict(sorted_nodes_deg)
    new_list = []
    for node, value in sorted_cycles_ratio:
        new_value = a * deg_dict[node] + (1 - a) * value
        new_list.append((node, new_value))
    weighted_list = sorted(new_list, key=lambda x: x[1], reverse=True) 
    
    sorted_nodes_cycles_ratio = []
    for t in weighted_list:
        sorted_nodes_cycles_ratio.append(t[0])

    g = np.linspace(0, 1, num=100).tolist() 
    a = sorted_nodes_cycles_ratio

    Pg = []
    for i in g:
        k = int((len(Mygraph.nodes()))*i)
        removal_nodes = a[:k]
        Mygraph1 = Mygraph.copy()
        for node in removal_nodes:
            Mygraph1.remove_edges_from(list(Mygraph1.edges(node)))

        all_nodes = list(Mygraph1.nodes()) 
        valid_nodes = [node for node in all_nodes if node not in removal_nodes] 
        I_nodes=np.random.choice(valid_nodes, size=int(len(valid_nodes)/2), replace=False).tolist()

        status = ["S"] * len(Mygraph1.nodes())
        # Set the node status in removal_nodes to "k"
        for node_index in removal_nodes:
            status[node_index] = "k"
        for node_index in I_nodes:
            status[node_index] = "I"   

        N = len(Mygraph1.nodes())
        beta = 0.25   
        gamma = 0.5  
        I_0 = int(N/2)       
        S_0 = N-I_0         
        
        infected_lists = []
        susceptible_lists = []
        for i in range(2000):
            status1 = copy.deepcopy(status)
            susceptible_counts, infected_counts = sis_model(Mygraph1, status1, beta, gamma)
            infected_lists.append(infected_counts) 
            susceptible_lists.append(susceptible_counts) 

        averages_infected_counts = []
        for i in range(len(infected_lists[0])):  
            total = sum(list_i[i] for list_i in infected_lists)
            average = total / len(infected_lists)
            averages_infected_counts.append(average)

        averages_susceptible_counts = []
        for i in range(len(susceptible_lists[0])):  
            total = sum(list_i[i] for list_i in susceptible_lists)
            average = total / len(susceptible_lists)
            averages_susceptible_counts.append(average)

        norm_averages_infected_counts = [x / N for x in averages_infected_counts]
        norm_averages_susceptible_counts = [x / N for x in averages_susceptible_counts]
        
        b = sum(norm_averages_infected_counts[-20:]) / len(norm_averages_infected_counts[-20:])
        Pg.append(b)
    Pg = [c/P0 for c in Pg]
    result_dict = dict(zip(g, Pg))
    
print('Under the DC index, List Pg/P0:', result_dict.values())


